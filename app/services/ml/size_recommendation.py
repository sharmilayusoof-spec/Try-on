"""
Size recommendation service based on body measurements
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class SizeRecommendationService:
    """Service for recommending clothing sizes based on body measurements"""
    
    # Standard size charts (in inches) - can be customized per clothing type
    SIZE_CHARTS = {
        'dress': {
            'XS': {'chest': 32, 'waist': 24, 'hips': 34, 'length': 35},
            'S': {'chest': 34, 'waist': 26, 'hips': 36, 'length': 36},
            'M': {'chest': 36, 'waist': 28, 'hips': 38, 'length': 37},
            'L': {'chest': 38, 'waist': 30, 'hips': 40, 'length': 38},
            'XL': {'chest': 40, 'waist': 32, 'hips': 42, 'length': 39},
            'XXL': {'chest': 42, 'waist': 34, 'hips': 44, 'length': 40}
        },
        'shirt': {
            'XS': {'chest': 34, 'waist': 28, 'shoulder': 16, 'length': 27},
            'S': {'chest': 36, 'waist': 30, 'shoulder': 17, 'length': 28},
            'M': {'chest': 38, 'waist': 32, 'shoulder': 18, 'length': 29},
            'L': {'chest': 40, 'waist': 34, 'shoulder': 19, 'length': 30},
            'XL': {'chest': 42, 'waist': 36, 'shoulder': 20, 'length': 31},
            'XXL': {'chest': 44, 'waist': 38, 'shoulder': 21, 'length': 32}
        },
        'top': {
            'XS': {'chest': 32, 'waist': 26, 'length': 24},
            'S': {'chest': 34, 'waist': 28, 'length': 25},
            'M': {'chest': 36, 'waist': 30, 'length': 26},
            'L': {'chest': 38, 'waist': 32, 'length': 27},
            'XL': {'chest': 40, 'waist': 34, 'length': 28},
            'XXL': {'chest': 42, 'waist': 36, 'length': 29}
        },
        'tshirt': {
            'XS': {'chest': 34, 'waist': 28, 'length': 26},
            'S': {'chest': 36, 'waist': 30, 'length': 27},
            'M': {'chest': 38, 'waist': 32, 'length': 28},
            'L': {'chest': 40, 'waist': 34, 'length': 29},
            'XL': {'chest': 42, 'waist': 36, 'length': 30},
            'XXL': {'chest': 44, 'waist': 38, 'length': 31}
        },
        'blouse': {
            'XS': {'chest': 32, 'waist': 24, 'shoulder': 14, 'length': 24},
            'S': {'chest': 34, 'waist': 26, 'shoulder': 15, 'length': 25},
            'M': {'chest': 36, 'waist': 28, 'shoulder': 16, 'length': 26},
            'L': {'chest': 38, 'waist': 30, 'shoulder': 17, 'length': 27},
            'XL': {'chest': 40, 'waist': 32, 'shoulder': 18, 'length': 28},
            'XXL': {'chest': 42, 'waist': 34, 'shoulder': 19, 'length': 29}
        },
        'jacket': {
            'XS': {'chest': 36, 'waist': 30, 'shoulder': 17, 'length': 26},
            'S': {'chest': 38, 'waist': 32, 'shoulder': 18, 'length': 27},
            'M': {'chest': 40, 'waist': 34, 'shoulder': 19, 'length': 28},
            'L': {'chest': 42, 'waist': 36, 'shoulder': 20, 'length': 29},
            'XL': {'chest': 44, 'waist': 38, 'shoulder': 21, 'length': 30},
            'XXL': {'chest': 46, 'waist': 40, 'shoulder': 22, 'length': 31}
        },
        'blazer': {
            'XS': {'chest': 36, 'waist': 30, 'shoulder': 17, 'length': 28},
            'S': {'chest': 38, 'waist': 32, 'shoulder': 18, 'length': 29},
            'M': {'chest': 40, 'waist': 34, 'shoulder': 19, 'length': 30},
            'L': {'chest': 42, 'waist': 36, 'shoulder': 20, 'length': 31},
            'XL': {'chest': 44, 'waist': 38, 'shoulder': 21, 'length': 32},
            'XXL': {'chest': 46, 'waist': 40, 'shoulder': 22, 'length': 33}
        }
    }
    
    # Pixels to inches conversion (approximate, based on average person height)
    # Assuming average person is 5'6" (66 inches) and takes up ~80% of image height
    PIXELS_PER_INCH_ESTIMATE = 10  # Will be calibrated per image
    
    def __init__(self):
        """Initialize size recommendation service"""
        pass
    
    def recommend_size(self, body_measurements: Dict, clothing_type: str,
                      image_height: int) -> Dict:
        """
        Recommend clothing size based on body measurements
        
        Args:
            body_measurements: Dictionary with pixel measurements
            clothing_type: Type of clothing (dress, shirt, etc.)
            image_height: Height of the image in pixels
            
        Returns:
            Dictionary with size recommendation and fit analysis
        """
        try:
            # Calibrate pixel to inch conversion
            pixels_per_inch = self._calibrate_conversion(body_measurements, image_height)
            
            # Convert pixel measurements to inches
            body_inches = self._convert_to_inches(body_measurements, pixels_per_inch)
            
            logger.info(f"Body measurements in inches: {body_inches}")
            
            # Get size chart for clothing type
            size_chart = self._get_size_chart(clothing_type)
            
            # Find best matching size
            recommended_size, fit_score, alternatives = self._find_best_size(
                body_inches, size_chart
            )
            
            # Generate fit analysis
            fit_analysis = self._analyze_fit(body_inches, size_chart[recommended_size])
            
            return {
                'recommended_size': recommended_size,
                'fit_score': fit_score,
                'alternative_sizes': alternatives,
                'body_measurements_inches': body_inches,
                'fit_analysis': fit_analysis,
                'size_chart': size_chart
            }
            
        except Exception as e:
            logger.error(f"Size recommendation failed: {e}")
            return {
                'recommended_size': 'M',
                'fit_score': 0.5,
                'alternative_sizes': ['S', 'L'],
                'error': str(e)
            }
    
    def _calibrate_conversion(self, measurements: Dict, image_height: int) -> float:
        """
        Calibrate pixel to inch conversion based on torso height
        Assumes average torso (shoulder to hip) is ~18 inches
        """
        torso_height_px = measurements.get('torso_height_px', image_height * 0.35)
        average_torso_inches = 18
        
        pixels_per_inch = torso_height_px / average_torso_inches
        
        logger.info(f"Calibrated conversion: {pixels_per_inch:.2f} pixels per inch")
        return pixels_per_inch
    
    def _convert_to_inches(self, measurements: Dict, pixels_per_inch: float) -> Dict:
        """Convert pixel measurements to inches"""
        return {
            'chest': measurements.get('chest_width_px', 0) / pixels_per_inch,
            'waist': measurements.get('waist_width_px', 0) / pixels_per_inch,
            'shoulder': measurements.get('shoulder_width_px', 0) / pixels_per_inch,
            'torso_length': measurements.get('torso_height_px', 0) / pixels_per_inch
        }
    
    def _get_size_chart(self, clothing_type: str) -> Dict:
        """Get size chart for clothing type"""
        # Normalize clothing type
        clothing_type = clothing_type.lower()
        
        # Map variations to standard types
        type_mapping = {
            'dresses': 'dress',
            'shirts': 'shirt',
            'tops': 'top',
            'tshirts': 'tshirt',
            't-shirt': 'tshirt',
            'blouses': 'blouse',
            'jackets': 'jacket',
            'blazers': 'blazer'
        }
        
        clothing_type = type_mapping.get(clothing_type, clothing_type)
        
        # Return appropriate size chart or default to shirt
        return self.SIZE_CHARTS.get(clothing_type, self.SIZE_CHARTS['shirt'])
    
    def _find_best_size(self, body_inches: Dict, size_chart: Dict) -> Tuple[str, float, List[str]]:
        """
        Find best matching size using weighted scoring
        
        Returns:
            (recommended_size, fit_score, alternative_sizes)
        """
        scores = {}
        
        for size, measurements in size_chart.items():
            score = 0
            weight_sum = 0
            
            # Chest measurement (most important)
            if 'chest' in body_inches and 'chest' in measurements:
                chest_diff = abs(body_inches['chest'] - measurements['chest'])
                chest_score = max(0, 1 - (chest_diff / 4))  # 4 inch tolerance
                score += chest_score * 3  # Weight: 3
                weight_sum += 3
            
            # Waist measurement
            if 'waist' in body_inches and 'waist' in measurements:
                waist_diff = abs(body_inches['waist'] - measurements['waist'])
                waist_score = max(0, 1 - (waist_diff / 4))
                score += waist_score * 2  # Weight: 2
                weight_sum += 2
            
            # Shoulder measurement
            if 'shoulder' in body_inches and 'shoulder' in measurements:
                shoulder_diff = abs(body_inches['shoulder'] - measurements['shoulder'])
                shoulder_score = max(0, 1 - (shoulder_diff / 2))
                score += shoulder_score * 2  # Weight: 2
                weight_sum += 2
            
            # Length measurement
            if 'torso_length' in body_inches and 'length' in measurements:
                length_diff = abs(body_inches['torso_length'] - measurements['length'])
                length_score = max(0, 1 - (length_diff / 3))
                score += length_score * 1  # Weight: 1
                weight_sum += 1
            
            # Normalize score
            scores[size] = score / weight_sum if weight_sum > 0 else 0
        
        # Sort by score
        sorted_sizes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        recommended_size = sorted_sizes[0][0]
        fit_score = sorted_sizes[0][1]
        
        # Get alternative sizes (top 2 alternatives)
        alternatives = [size for size, _ in sorted_sizes[1:3]]
        
        logger.info(f"Size scores: {scores}")
        logger.info(f"Recommended: {recommended_size} (score: {fit_score:.2f})")
        
        return recommended_size, fit_score, alternatives
    
    def _analyze_fit(self, body_inches: Dict, size_measurements: Dict) -> Dict:
        """
        Analyze how well the size fits
        
        Returns:
            Dictionary with fit analysis for each measurement
        """
        analysis = {}
        
        for measurement in ['chest', 'waist', 'shoulder']:
            if measurement in body_inches and measurement in size_measurements:
                body_val = body_inches[measurement]
                size_val = size_measurements[measurement]
                diff = size_val - body_val
                
                if diff > 2:
                    fit = 'loose'
                elif diff > 0.5:
                    fit = 'comfortable'
                elif diff > -0.5:
                    fit = 'fitted'
                elif diff > -2:
                    fit = 'snug'
                else:
                    fit = 'tight'
                
                analysis[measurement] = {
                    'fit': fit,
                    'difference_inches': round(diff, 1),
                    'body_measurement': round(body_val, 1),
                    'garment_measurement': round(size_val, 1)
                }
        
        return analysis
    
    def get_size_chart_for_display(self, clothing_type: str) -> Dict:
        """Get formatted size chart for frontend display"""
        size_chart = self._get_size_chart(clothing_type)
        
        formatted = {}
        for size, measurements in size_chart.items():
            formatted[size] = {
                key: f"{value}\"" for key, value in measurements.items()
            }
        
        return formatted

# Made with Bob
