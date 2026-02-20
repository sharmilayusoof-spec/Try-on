"""
Generate better quality clothing images with solid fills and realistic appearance
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_realistic_clothing(filename, text, base_color, clothing_type):
    """Create realistic clothing image with proper fills"""
    width, height = 400, 500
    
    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Convert hex color to RGB
    if isinstance(base_color, str) and base_color.startswith('#'):
        base_color = tuple(int(base_color[i:i+2], 16) for i in (1, 3, 5))
    
    # Add slight texture variation
    def add_shade(color, factor=0.9):
        return tuple(int(c * factor) for c in color)
    
    dark_color = add_shade(base_color, 0.7)
    light_color = tuple(min(255, int(c * 1.2)) for c in base_color)
    
    if 'dress' in clothing_type or 'gown' in clothing_type:
        # Draw dress with gradient effect
        # Bodice
        draw.rectangle([100, 80, 300, 200], fill=base_color, outline=dark_color, width=3)
        # Add bodice details
        draw.rectangle([110, 90, 290, 195], outline=light_color, width=1)
        
        # Skirt (trapezoid with gradient effect)
        for i in range(200, 450, 5):
            width_at_y = 200 + (i - 200) * 0.6
            x_left = 200 - width_at_y / 2
            x_right = 200 + width_at_y / 2
            shade_factor = 0.85 + (i - 200) / 1000
            color = add_shade(base_color, shade_factor)
            draw.rectangle([x_left, i, x_right, i+5], fill=color, outline=color)
        
        # Outline
        draw.polygon([100, 200, 300, 200, 350, 450, 50, 450], outline=dark_color, width=3)
        
        # Straps
        draw.rectangle([120, 50, 140, 80], fill=base_color, outline=dark_color, width=2)
        draw.rectangle([260, 50, 280, 80], fill=base_color, outline=dark_color, width=2)
        
        # Add waistline detail
        draw.line([100, 200, 300, 200], fill=dark_color, width=4)
        
    elif 'jacket' in clothing_type or 'blazer' in clothing_type:
        # Draw jacket
        draw.rectangle([80, 100, 320, 450], fill=base_color, outline=dark_color, width=3)
        
        # Collar
        draw.polygon([150, 100, 200, 80, 250, 100], fill=base_color, outline=dark_color, width=2)
        
        # Lapels
        draw.polygon([120, 100, 150, 100, 120, 200], fill=light_color, outline=dark_color, width=2)
        draw.polygon([280, 100, 250, 100, 280, 200], fill=light_color, outline=dark_color, width=2)
        
        # Buttons
        for y in [150, 200, 250, 300, 350]:
            draw.ellipse([190, y, 210, y+20], fill='#FFD700', outline='#B8860B', width=2)
            # Button holes
            draw.line([195, y+10, 205, y+10], fill='#8B7500', width=2)
        
        # Pockets
        draw.rectangle([100, 280, 160, 340], fill=add_shade(base_color, 0.85), outline=dark_color, width=2)
        draw.rectangle([240, 280, 300, 340], fill=add_shade(base_color, 0.85), outline=dark_color, width=2)
        
        # Pocket flaps
        draw.rectangle([95, 270, 165, 285], fill=base_color, outline=dark_color, width=2)
        draw.rectangle([235, 270, 305, 285], fill=base_color, outline=dark_color, width=2)
        
    elif 'shirt' in clothing_type or 'blouse' in clothing_type:
        # Draw shirt
        draw.rectangle([100, 120, 300, 450], fill=base_color, outline=dark_color, width=3)
        
        # Collar
        draw.polygon([160, 120, 200, 100, 240, 120], fill=base_color, outline=dark_color, width=2)
        draw.polygon([160, 120, 180, 110, 180, 140], fill=light_color, outline=dark_color, width=1)
        draw.polygon([240, 120, 220, 110, 220, 140], fill=light_color, outline=dark_color, width=1)
        
        # Button placket
        draw.rectangle([195, 120, 205, 450], fill=light_color, outline=dark_color, width=1)
        
        # Buttons
        for y in [160, 210, 260, 310, 360, 410]:
            draw.ellipse([197, y, 203, y+6], fill='white', outline=dark_color, width=1)
        
        # Sleeves
        draw.rectangle([60, 140, 100, 280], fill=base_color, outline=dark_color, width=2)
        draw.rectangle([300, 140, 340, 280], fill=base_color, outline=dark_color, width=2)
        # Cuffs
        draw.rectangle([60, 260, 100, 280], fill=light_color, outline=dark_color, width=2)
        draw.rectangle([300, 260, 340, 280], fill=light_color, outline=dark_color, width=2)
        
    elif 'tshirt' in clothing_type or 'top' in clothing_type:
        # Draw t-shirt
        draw.rectangle([100, 140, 300, 450], fill=base_color, outline=dark_color, width=3)
        
        # Neck
        draw.ellipse([170, 120, 230, 160], fill=(255, 255, 255, 0), outline=dark_color, width=3)
        
        # Sleeves
        draw.rectangle([60, 140, 100, 240], fill=base_color, outline=dark_color, width=2)
        draw.rectangle([300, 140, 340, 240], fill=base_color, outline=dark_color, width=2)
        
        # Add some texture/shading
        for i in range(150, 440, 20):
            draw.line([110, i, 290, i], fill=add_shade(base_color, 0.95), width=1)
    
    # Convert to RGB (remove alpha for JPEG compatibility)
    rgb_img = Image.new('RGB', (width, height), 'white')
    rgb_img.paste(img, (0, 0), img)
    
    return rgb_img

# Clothing configuration
clothes_config = [
    ("dress1.png", "Black Evening Dress", "#1C1C1C", "dress"),
    ("dress2.png", "Summer Floral Dress", "#FFB6C1", "dress"),
    ("dress3.png", "Red A-Line Dress", "#DC143C", "dress"),
    ("dress4.png", "Blue Maxi Dress", "#4169E1", "dress"),
    ("dress5.png", "Pink Cocktail Dress", "#FF69B4", "dress"),
    ("dress6.png", "White Lace Dress", "#F5F5F5", "dress"),
    ("dress7.png", "Navy Formal Dress", "#000080", "dress"),
    ("dress8.png", "Green Wrap Dress", "#228B22", "dress"),
    ("dress9.png", "Yellow Sundress", "#FFD700", "dress"),
    ("dress10.png", "Purple Evening Gown", "#9370DB", "gown"),
    ("dress11.png", "Floral Midi Dress", "#FF1493", "dress"),
    ("dress12.png", "Coral Summer Dress", "#FF7F50", "dress"),
    ("dress13.png", "Burgundy Evening Gown", "#800020", "gown"),
    ("dress14.png", "Mint Green Midi Dress", "#98FF98", "dress"),
    ("dress15.png", "Peach Cocktail Dress", "#FFDAB9", "dress"),
    ("jacket1.png", "Denim Jacket", "#4682B4", "jacket"),
    ("jacket2.png", "Leather Jacket", "#2F4F4F", "jacket"),
    ("blazer1.png", "Black Blazer", "#1C1C1C", "blazer"),
    ("blouse1.png", "Casual Blouse", "#87CEEB", "blouse"),
    ("top1.png", "Silk Top", "#F5F5DC", "top"),
    ("shirt1.png", "Classic Shirt", "#DC143C", "shirt"),
    ("shirt2.png", "Casual Shirt", "#228B22", "shirt"),
    ("tshirt1.png", "Cotton T-Shirt", "#4169E1", "tshirt"),
    ("tshirt2.png", "Graphic T-Shirt", "#2F4F4F", "tshirt"),
]

# Create output directory
output_dir = 'frontend/assets/clothes'
os.makedirs(output_dir, exist_ok=True)

print("Generating improved clothing images...")
for filename, text, color, clothing_type in clothes_config:
    output_path = os.path.join(output_dir, filename)
    img = create_realistic_clothing(filename, text, color, clothing_type)
    img.save(output_path, 'PNG', quality=95)
    print(f"Created: {filename}")

print(f"\nSuccessfully generated {len(clothes_config)} improved clothing images!")

# Made with Bob
