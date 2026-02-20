"""
Generate placeholder clothing images with proper styling
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Clothing items configuration
clothes = [
    ("dress1.png", "Black Evening\nDress", "#000000"),
    ("dress2.png", "Summer Floral\nDress", "#FFB6C1"),
    ("dress3.png", "Red A-Line\nDress", "#DC143C"),
    ("dress4.png", "Blue Maxi\nDress", "#4169E1"),
    ("dress5.png", "Pink Cocktail\nDress", "#FF69B4"),
    ("dress6.png", "White Lace\nDress", "#FFFFFF"),
    ("dress7.png", "Navy Formal\nDress", "#000080"),
    ("dress8.png", "Green Wrap\nDress", "#228B22"),
    ("dress9.png", "Yellow\nSundress", "#FFD700"),
    ("dress10.png", "Purple Evening\nGown", "#9370DB"),
    ("dress11.png", "Floral Midi\nDress", "#FF1493"),
    ("dress12.png", "Coral Summer\nDress", "#FF7F50"),
    ("dress13.png", "Burgundy\nEvening Gown", "#800020"),
    ("dress14.png", "Mint Green\nMidi Dress", "#98FF98"),
    ("dress15.png", "Peach Cocktail\nDress", "#FFDAB9"),
    ("jacket1.png", "Denim\nJacket", "#4682B4"),
    ("jacket2.png", "Leather\nJacket", "#2F4F4F"),
    ("blazer1.png", "Black\nBlazer", "#1C1C1C"),
    ("blouse1.png", "Casual\nBlouse", "#87CEEB"),
    ("top1.png", "Silk\nTop", "#F5F5DC"),
    ("shirt1.png", "Classic\nShirt", "#DC143C"),
    ("shirt2.png", "Casual\nShirt", "#228B22"),
    ("tshirt1.png", "Cotton\nT-Shirt", "#4169E1"),
    ("tshirt2.png", "Graphic\nT-Shirt", "#000000"),
]

def create_clothing_image(filename, text, color):
    """Create a stylized clothing placeholder image"""
    # Create image
    width, height = 400, 500
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw clothing shape based on type
    if 'dress' in filename or 'gown' in filename:
        # Draw dress shape
        # Top part (bodice)
        draw.rectangle([100, 80, 300, 200], fill=color, outline='#333333', width=3)
        # Skirt (trapezoid)
        draw.polygon([100, 200, 300, 200, 350, 450, 50, 450], fill=color, outline='#333333', width=3)
        # Straps
        draw.rectangle([120, 50, 140, 80], fill=color, outline='#333333', width=2)
        draw.rectangle([260, 50, 280, 80], fill=color, outline='#333333', width=2)
        
    elif 'jacket' in filename or 'blazer' in filename:
        # Draw jacket shape
        draw.rectangle([80, 100, 320, 450], fill=color, outline='#333333', width=3)
        # Collar
        draw.polygon([150, 100, 200, 80, 250, 100], fill=color, outline='#333333', width=2)
        # Buttons
        for y in [150, 200, 250, 300, 350]:
            draw.ellipse([190, y, 210, y+20], fill='#FFD700', outline='#333333', width=2)
        # Pockets
        draw.rectangle([100, 280, 160, 340], outline='#333333', width=2)
        draw.rectangle([240, 280, 300, 340], outline='#333333', width=2)
        
    elif 'shirt' in filename or 'blouse' in filename:
        # Draw shirt shape
        draw.rectangle([100, 120, 300, 450], fill=color, outline='#333333', width=3)
        # Collar
        draw.polygon([160, 120, 200, 100, 240, 120], fill=color, outline='#333333', width=2)
        # Buttons
        for y in [160, 210, 260, 310, 360]:
            draw.ellipse([195, y, 205, y+10], fill='white', outline='#333333', width=1)
        # Sleeves
        draw.rectangle([60, 140, 100, 280], fill=color, outline='#333333', width=2)
        draw.rectangle([300, 140, 340, 280], fill=color, outline='#333333', width=2)
        
    elif 'tshirt' in filename or 'top' in filename:
        # Draw t-shirt shape
        draw.rectangle([100, 140, 300, 450], fill=color, outline='#333333', width=3)
        # Neck
        draw.ellipse([170, 120, 230, 160], fill='white', outline='#333333', width=2)
        # Sleeves
        draw.rectangle([60, 140, 100, 240], fill=color, outline='#333333', width=2)
        draw.rectangle([300, 140, 340, 240], fill=color, outline='#333333', width=2)
    
    # Add text label at bottom
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Draw text background
    draw.rectangle([0, 460, width, height], fill='#1a1a2e')
    
    # Draw text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = 465
    
    draw.text((text_x, text_y), text, fill='white', font=font, align='center')
    
    return img

# Create output directory
output_dir = 'frontend/assets/clothes'
os.makedirs(output_dir, exist_ok=True)

# Generate all images
print("Generating clothing placeholder images...")
for filename, text, color in clothes:
    output_path = os.path.join(output_dir, filename)
    img = create_clothing_image(filename, text, color)
    img.save(output_path, 'PNG')
    print(f"Created: {filename}")

print(f"\nSuccessfully generated {len(clothes)} clothing images!")
print(f"Images saved to: {output_dir}")

# Made with Bob
