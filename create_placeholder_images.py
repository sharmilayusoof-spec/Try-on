"""
Create placeholder clothing images for Virtual Try-On app
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_images():
    """Create colored placeholder images for clothing items"""
    
    # Ensure directory exists
    output_dir = 'frontend/assets/clothes'
    os.makedirs(output_dir, exist_ok=True)
    
    # Define placeholder images with colors
    placeholders = [
        ('shirt1.png', 'Blue Casual\nShirt', (100, 150, 200)),
        ('shirt2.png', 'White Formal\nShirt', (240, 240, 240)),
        ('shirt3.png', 'Red\nT-Shirt', (200, 100, 100)),
        ('pants1.png', 'Blue\nJeans', (80, 120, 180)),
        ('pants2.png', 'Black\nTrousers', (50, 50, 50)),
        ('dress1.png', 'Summer\nDress', (255, 200, 150)),
    ]
    
    print("="*60)
    print("CREATING PLACEHOLDER CLOTHING IMAGES")
    print("="*60)
    print(f"\nOutput directory: {output_dir}\n")
    
    for filename, text, color in placeholders:
        # Create 512x512 image
        img = Image.new('RGB', (512, 512), color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", 48)
            except:
                try:
                    # Try system fonts on different OS
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
                except:
                    font = ImageFont.load_default()
        
        # Calculate text position (centered)
        # Split text by newlines for multi-line
        lines = text.split('\n')
        
        # Calculate total height
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_heights.append(bbox[3] - bbox[1])
        
        total_height = sum(line_heights) + (len(lines) - 1) * 10  # 10px spacing
        
        # Start y position (centered vertically)
        y = (512 - total_height) // 2
        
        # Draw each line centered
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (512 - text_width) // 2
            
            # Add shadow for better visibility
            draw.text((x+2, y+2), line, fill=(0, 0, 0, 128), font=font)
            draw.text((x, y), line, fill='white', font=font)
            
            y += bbox[3] - bbox[1] + 10  # Move to next line
        
        # Add border
        draw.rectangle([(0, 0), (511, 511)], outline='white', width=3)
        
        # Save
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        print(f'✓ Created {filepath}')
        print(f'  Size: {img.size}, Color: RGB{color}')
    
    print("\n" + "="*60)
    print("✅ ALL PLACEHOLDER IMAGES CREATED!")
    print("="*60)
    print("\nNext steps:")
    print("1. Refresh your browser")
    print("2. Check that images load without 404 errors")
    print("3. Replace with real clothing images when ready")
    print("\nTo replace with real images:")
    print(f"  - Add your images to: {output_dir}/")
    print("  - Use same filenames (shirt1.png, pants1.png, etc.)")
    print("  - Recommended size: 512x512 or 1024x1024 pixels")
    print()


if __name__ == "__main__":
    try:
        create_placeholder_images()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure PIL/Pillow is installed: pip install Pillow")
        print("- Check that frontend/assets/clothes/ directory exists")
        print("- Verify you have write permissions")
