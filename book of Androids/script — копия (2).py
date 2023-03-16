from PIL import Image, ImageDraw, ImageFont

# Define the font for the dialog text
font_path = "font.ttf"
font_size = 14
font = ImageFont.truetype(font_path, font_size)

# Define the colors for the dialog text and background
text_color = (0, 0, 0)  # Black
bg_color = (255, 255, 255)  # White
name_color = (255, 0, 0)  # Red
other_color = (255, 255, 0)  # Yellow

# Load the image
image_path = "image.jpg"
image = Image.open(image_path)

# Load the dialog from the text file
dialog_path = "dialogs.txt"
with open(dialog_path) as f:
    dialog_lines = f.readlines()

# Find the positions to place the dialog bubbles
positions = []
for line in dialog_lines:
    character, text = line.split(": ")
    count = len(text)
    positions.append((count, character))

positions.sort()
x = 10
y = 10
for _, character in positions:
    dialog = character.strip() + ": "
    text = dialog_lines[positions.index((_, character))].split(": ")[1].strip()
    w, h = font.getsize(dialog + text)
    draw = ImageDraw.Draw(image)
    draw.ellipse([x, y, x + w + 10, y + h + 10], fill=bg_color)
    draw.text((x + 5, y + 5), dialog, fill=name_color, font=font)
    draw.text((x + 60, y + 5), text, fill=text_color, font=font)
    y += h + 20

# Save the new image with the dialog
image.save("image_with_dialog.jpg")
