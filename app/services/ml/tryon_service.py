"""
Virtual Try-On service - Main processing pipeline
"""
import cv2
import numpy as np
import time
from pathlib import Path
from typing import Dict, Tuple, Optional
from app.services.ml.pose_detection import PoseDetector
from app.services.ml.size_recommendation import SizeRecommendationService
from app.utils.image_processor import (
    load_image, save_image, resize_image, blend_images
)
from app.core.config import settings
from app.core.exceptions import ImageProcessingError, PoseDetectionError


class TryOnService:
    """Virtual Try-On processing service with size recommendation"""
    
    def __init__(self):
        """Initialize try-on service"""
        self.pose_detector = PoseDetector()
        self.size_recommender = SizeRecommendationService()
    
    def process(self, user_image_path: str, cloth_image_path: str,
                output_path: str, clothing_type: Optional[str] = None) -> Dict:
        """
        Process virtual try-on
        
        Args:
            user_image_path: Path to user image
            cloth_image_path: Path to cloth image
            output_path: Path to save result
            
        Returns:
            Dictionary with result metadata
        """
        start_time = time.time()
        
        try:
            # Load images
            user_img = load_image(user_image_path)
            cloth_img = load_image(cloth_image_path)
            
            # Detect pose
            pose_result = self.pose_detector.detect(user_img)
            landmarks = pose_result['landmarks']
            keypoints = self.pose_detector.get_keypoints(landmarks)
            
            # Debug: Log keypoints
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Detected keypoints: shoulders at y={keypoints.get('left_shoulder', (0,0))[1]:.2f}, hips at y={keypoints.get('left_hip', (0,0))[1]:.2f}")
            
            # Get body region with measurements
            body_region = self._get_body_region(user_img, keypoints)
            logger.info(f"Body region: y1={body_region['y1']}, y2={body_region['y2']}, height={body_region['height']}")
            
            # Get size recommendation if clothing type provided
            size_recommendation = None
            if clothing_type:
                size_recommendation = self.size_recommender.recommend_size(
                    body_region['measurements'],
                    clothing_type,
                    user_img.shape[0]
                )
                logger.info(f"Size recommendation: {size_recommendation['recommended_size']}")
            
            # Warp cloth to fit body with improved perspective
            warped_cloth = self._warp_cloth(cloth_img, body_region, keypoints)
            
            # Blend cloth with user image
            result = self._blend_cloth(user_img, warped_cloth, body_region)
            
            # Save result
            save_image(result, output_path)
            
            # Calculate processing time
            time_taken = time.time() - start_time
            
            response = {
                'success': True,
                'output_path': output_path,
                'time_taken': time_taken,
                'metadata': {
                    'person_size': f"{user_img.shape[1]}x{user_img.shape[0]}",
                    'cloth_size': f"{cloth_img.shape[1]}x{cloth_img.shape[0]}",
                    'landmarks_detected': len(landmarks),
                    'pose_confidence': pose_result['confidence'],
                    'body_measurements': body_region['measurements']
                }
            }
            
            # Add size recommendation if available
            if size_recommendation:
                response['size_recommendation'] = size_recommendation
            
            return response
            
        except (PoseDetectionError, ImageProcessingError) as e:
            raise
        except Exception as e:
            raise ImageProcessingError(f"Try-on processing failed: {str(e)}")
    
    def _get_body_region(self, image: np.ndarray,
                         keypoints: Dict[str, Tuple[float, float]]) -> Dict:
        """
        Extract TORSO region for cloth placement - ensures clothing appears on body, NOT face
        
        Args:
            image: User image
            keypoints: Body keypoints
            
        Returns:
            Dictionary with region coordinates and body measurements
        """
        h, w = image.shape[:2]
        
        # Get key body points with realistic fallbacks
        nose = keypoints.get('nose', (0.5, 0.15))
        left_shoulder = keypoints.get('left_shoulder', (0.35, 0.30))
        right_shoulder = keypoints.get('right_shoulder', (0.65, 0.30))
        left_hip = keypoints.get('left_hip', (0.40, 0.65))
        right_hip = keypoints.get('right_hip', (0.60, 0.65))
        
        # Convert normalized coordinates to pixels
        nose_y = int(nose[1] * h)
        shoulder_left_x = int(left_shoulder[0] * w)
        shoulder_right_x = int(right_shoulder[0] * w)
        shoulder_y = int(min(left_shoulder[1], right_shoulder[1]) * h)
        
        hip_left_x = int(left_hip[0] * w)
        hip_right_x = int(right_hip[0] * w)
        hip_y = int(max(left_hip[1], right_hip[1]) * h)
        
        # Calculate body measurements for size recommendation
        shoulder_width = abs(shoulder_right_x - shoulder_left_x)
        torso_height = abs(hip_y - shoulder_y)
        
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Body measurements: shoulder_width={shoulder_width}px, torso_height={torso_height}px")
        
        # CRITICAL FIX: Start clothing BELOW the neck, never on face
        # Calculate neck position (below nose, above shoulders)
        neck_y = nose_y + int((shoulder_y - nose_y) * 0.7)  # 70% down from nose to shoulders
        
        # Ensure clothing starts at least at neck level or below
        clothing_start_y = max(neck_y, shoulder_y - 20)  # Start at neck or slightly above shoulders
        
        # NEVER allow clothing above 25% of image height (safety check)
        absolute_min_y = int(h * 0.25)
        clothing_start_y = max(clothing_start_y, absolute_min_y)
        
        logger.info(f"Clothing placement: nose_y={nose_y}, neck_y={neck_y}, shoulder_y={shoulder_y}, start_y={clothing_start_y}")
        
        # Calculate torso region boundaries
        x1 = min(shoulder_left_x, hip_left_x)
        x2 = max(shoulder_right_x, hip_right_x)
        y1 = clothing_start_y
        y2 = hip_y + int(torso_height * 0.4)  # Extend below hips for full coverage
        
        # Add horizontal padding for natural fit
        horizontal_padding = int(shoulder_width * 0.25)
        x1 = max(0, x1 - horizontal_padding)
        x2 = min(w, x2 + horizontal_padding)
        
        # Ensure minimum dimensions
        min_width = int(w * 0.30)
        min_height = int(h * 0.40)
        
        if (x2 - x1) < min_width:
            center_x = (x1 + x2) // 2
            x1 = max(0, center_x - min_width // 2)
            x2 = min(w, center_x + min_width // 2)
        
        if (y2 - y1) < min_height:
            # Expand downward only, never upward
            y2 = min(h, y1 + min_height)
        
        # Ensure we don't exceed image boundaries
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        return {
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'width': x2 - x1,
            'height': y2 - y1,
            'keypoints': {
                'nose': (int(nose[0] * w), nose_y),
                'neck': (int((left_shoulder[0] + right_shoulder[0]) / 2 * w), neck_y),
                'left_shoulder': (shoulder_left_x, shoulder_y),
                'right_shoulder': (shoulder_right_x, shoulder_y),
                'left_hip': (hip_left_x, hip_y),
                'right_hip': (hip_right_x, hip_y)
            },
            'measurements': {
                'shoulder_width_px': shoulder_width,
                'torso_height_px': torso_height,
                'chest_width_px': int(shoulder_width * 1.1),  # Estimate
                'waist_width_px': abs(hip_right_x - hip_left_x)
            }
        }
    
    def _warp_cloth(self, cloth: np.ndarray, body_region: Dict,
                    keypoints: Dict[str, Tuple[float, float]]) -> np.ndarray:
        """
        Warp cloth to fit body region with improved sizing and perspective
        
        Args:
            cloth: Cloth image
            body_region: Body region coordinates
            keypoints: Body keypoints
            
        Returns:
            Warped and resized cloth image
        """
        # Get cloth dimensions
        cloth_h, cloth_w = cloth.shape[:2]
        
        # Target dimensions
        target_w = body_region['width']
        target_h = body_region['height']
        
        # Resize to FULLY cover the torso region
        # Calculate scale to fit the region - INCREASED for better coverage
        scale_w = target_w / cloth_w
        scale_h = target_h / cloth_h
        
        # Use the LARGER scale to ensure full coverage, then add extra
        scale = max(scale_w, scale_h) * 1.3  # Increased from 1.2 to 1.3 for fuller coverage
        
        new_w = int(cloth_w * scale)
        new_h = int(cloth_h * scale)
        
        # Resize cloth
        resized_cloth = cv2.resize(cloth, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Create canvas of target size
        warped = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        
        # Center the cloth in the canvas
        offset_x = (target_w - new_w) // 2
        offset_y = (target_h - new_h) // 2
        
        # Ensure cloth fits within canvas
        if offset_x < 0:
            crop_x = -offset_x
            new_w = target_w
            offset_x = 0
            resized_cloth = resized_cloth[:, crop_x:crop_x+new_w]
        
        if offset_y < 0:
            crop_y = -offset_y
            new_h = target_h
            offset_y = 0
            resized_cloth = resized_cloth[crop_y:crop_y+new_h, :]
        
        # Place cloth on canvas
        end_y = min(offset_y + resized_cloth.shape[0], target_h)
        end_x = min(offset_x + resized_cloth.shape[1], target_w)
        
        warped[offset_y:end_y, offset_x:end_x] = resized_cloth[:end_y-offset_y, :end_x-offset_x]
        
        return warped
    
    def _blend_cloth(self, user_img: np.ndarray, cloth: np.ndarray,
                     body_region: Dict) -> np.ndarray:
        """
        Blend cloth with user image using advanced alpha blending and color matching
        
        Args:
            user_img: User image
            cloth: Warped cloth
            body_region: Body region coordinates
            
        Returns:
            Blended result image
        """
        result = user_img.copy()
        
        # Extract region
        x1, y1 = body_region['x1'], body_region['y1']
        x2, y2 = body_region['x2'], body_region['y2']
        
        # Ensure cloth matches region size
        if cloth.shape[0] != (y2 - y1) or cloth.shape[1] != (x2 - x1):
            cloth = cv2.resize(cloth, (x2 - x1, y2 - y1), interpolation=cv2.INTER_LANCZOS4)
        
        # Apply slight color correction to match lighting
        user_region = result[y1:y2, x1:x2]
        cloth = self._match_lighting(cloth, user_region)
        
        # Create a sophisticated mask with better edge blending
        h, w = cloth.shape[:2]
        mask = np.ones((h, w), dtype=np.float32)
        
        # Create gradient mask for smooth blending
        feather = 30  # Increased for smoother transitions
        
        # Top edge - gradual fade with cubic easing
        for i in range(min(feather, h)):
            alpha = (i / feather) ** 3  # Cubic for even smoother transition
            mask[i, :] *= alpha
        
        # Bottom edge - gradual fade
        for i in range(min(feather, h)):
            alpha = (i / feather) ** 3
            if h - i - 1 >= 0:
                mask[h - i - 1, :] *= alpha
        
        # Side edges - gradual fade
        for i in range(feather):
            alpha = (i / feather) ** 2
            mask[:, i] *= alpha
            mask[:, -(i+1)] *= alpha
        
        # Create center emphasis (stronger in middle)
        center_mask = np.ones((h, w), dtype=np.float32)
        cy, cx = h // 2, w // 2
        for y in range(h):
            for x in range(w):
                dist_from_center = np.sqrt((y - cy)**2 + (x - cx)**2)
                max_dist = np.sqrt(cy**2 + cx**2)
                center_mask[y, x] = 1.0 - (dist_from_center / max_dist) * 0.3
        
        mask = mask * center_mask
        
        # Get ROI first to ensure dimensions match
        roi = result[y1:y2, x1:x2]
        roi_h, roi_w = roi.shape[:2]
        
        # Ensure cloth exactly matches ROI dimensions
        if cloth.shape[0] != roi_h or cloth.shape[1] != roi_w:
            cloth = cv2.resize(cloth, (roi_w, roi_h), interpolation=cv2.INTER_LANCZOS4)
            # Recreate mask with correct dimensions
            mask = np.ones((roi_h, roi_w), dtype=np.float32)
            
            # Recreate gradient mask
            feather = min(30, roi_h // 3, roi_w // 3)
            for i in range(min(feather, roi_h)):
                alpha = (i / feather) ** 3
                mask[i, :] *= alpha
                if roi_h - i - 1 >= 0:
                    mask[roi_h - i - 1, :] *= alpha
            
            for i in range(min(feather, roi_w)):
                alpha = (i / feather) ** 2
                mask[:, i] *= alpha
                if roi_w - i - 1 >= 0:
                    mask[:, -(i+1)] *= alpha
        
        # Expand mask to 3 channels
        mask_3ch = np.stack([mask] * 3, axis=2)
        
        # Convert to float for blending
        roi_float = roi.astype(np.float32)
        cloth_float = cloth.astype(np.float32)
        
        # Blend with high opacity in center, fading at edges
        alpha = 0.9  # High opacity for cloth
        blended_roi = (cloth_float * mask_3ch * alpha + roi_float * (1 - mask_3ch * alpha))
        
        result[y1:y2, x1:x2] = np.clip(blended_roi, 0, 255).astype(np.uint8)
        
        return result
    
    def _match_lighting(self, cloth: np.ndarray, reference: np.ndarray) -> np.ndarray:
        """
        Match cloth lighting to reference region for better blending
        
        Args:
            cloth: Cloth image to adjust
            reference: Reference region from user image
            
        Returns:
            Adjusted cloth image
        """
        # Convert to LAB color space for better color matching
        cloth_lab = cv2.cvtColor(cloth, cv2.COLOR_BGR2LAB).astype(np.float32)
        ref_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB).astype(np.float32)
        
        # Calculate mean and std for each channel
        cloth_mean = cloth_lab.mean(axis=(0, 1))
        cloth_std = cloth_lab.std(axis=(0, 1))
        ref_mean = ref_lab.mean(axis=(0, 1))
        ref_std = ref_lab.std(axis=(0, 1))
        
        # Adjust cloth to match reference lighting (only L channel for brightness)
        # Keep color channels mostly intact
        for i in range(3):
            if cloth_std[i] > 0:
                if i == 0:  # L channel (lightness) - match more closely
                    cloth_lab[:, :, i] = ((cloth_lab[:, :, i] - cloth_mean[i]) / cloth_std[i]) * ref_std[i] * 0.7 + ref_mean[i] * 0.3 + cloth_mean[i] * 0.7
                else:  # A and B channels (color) - preserve more
                    cloth_lab[:, :, i] = ((cloth_lab[:, :, i] - cloth_mean[i]) / cloth_std[i]) * cloth_std[i] * 0.9 + cloth_mean[i]
        
        # Clip values to valid range
        cloth_lab = np.clip(cloth_lab, 0, 255)
        
        # Convert back to BGR
        result = cv2.cvtColor(cloth_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
        return result

