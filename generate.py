from PIL import Image, ImageDraw, ImageFont
import os

# Function to create a single post
def create_post(template_path, quote, output_path, font_path="font.ttf", font_size=50):
    # Open the template image
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    
    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    
    # Define text position and properties
    text_color = "#6565D6"  # White text
    width, height = image.size
    margin = 60

    # Split text into multiple lines if necessary
    lines = []
    words = quote.split()
    while words:
        line = ''
        while words and (draw.textbbox((0, 0), line + words[0], font=font)[2] < (width - 2 * margin)):
            line = line + (words.pop(0) + ' ')
        lines.append(line)
    
    # Calculate total text height
    total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])
    
    # Draw text on image
    y = (height - total_text_height) // 2
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
        x = (width - text_width) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += text_height
    
    # Save the image
    image.save(output_path)

# Path to the template image
template_path = "template.png"

# Folder to save the posts
output_folder = "posts"
os.makedirs(output_folder, exist_ok=True)

# Path to the font
font_path = "font.ttf"

# Font size
font_size = 50

# Load quotes from file
with open("quotes.txt", "r") as file:
    quotes = file.readlines()

# Create posts
for i, quote in enumerate(quotes):
    quote = quote.strip()  # Remove any leading/trailing whitespace
    output_path = os.path.join(output_folder, f"post_{i+1}.png")
    create_post(template_path, quote, output_path, font_path, font_size)

print("Posts created successfully!")
