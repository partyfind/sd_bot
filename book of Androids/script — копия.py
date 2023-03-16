from PIL import Image, ImageDraw, ImageFont

# Open image and get dimensions
image = Image.open('image.jpg')
width, height = image.size

# Load dialog text from file
with open('dialogs.txt', 'r') as f:
    dialog_lines = f.readlines()

# Define fonts and colors
name_font = ImageFont.truetype('arial.ttf', 16)
text_font = ImageFont.truetype('arial.ttf', 12)
name_color = (255, 0, 0)  # red
text_color = (255, 255, 255)  # white
cloud_color = (255, 255, 0)  # yellow

# Calculate location for dialog
dialog_width = int(width * 0.8)  # dialog width is 80% of image width
dialog_height = len(dialog_lines) * 20  # assume 20 pixels per line
dialog_x = int((width - dialog_width) / 2)  # center horizontally
dialog_y = int((height - dialog_height) / 2)  # center vertically

# Draw dialog cloud
draw = ImageDraw.Draw(image)
cloud_x1 = dialog_x - 10
cloud_y1 = dialog_y - 10
cloud_x2 = dialog_x + dialog_width + 10
cloud_y2 = dialog_y + dialog_height + 10
draw.rectangle((cloud_x1, cloud_y1, cloud_x2, cloud_y2), fill=cloud_color, outline=cloud_color)

# Add name and text to dialog
for i, line in enumerate(dialog_lines):
    name, text = line.split(':')
    name = name.strip()
    text = text.strip()
    name_width = 160
    name_height = 60
    text_width = 600
    text_height = 600
    name_x = dialog_x + 10  # name is 10 pixels from left edge
    name_y = dialog_y + 10 + i * 20  # each line is 20 pixels high
    text_x = dialog_x + 20 + name_width  # text starts after name
    text_y = name_y
    draw.text((name_x, name_y), name, fill=name_color, font=name_font)
    draw.text((text_x, text_y), text, fill=text_color, font=text_font)

# Save modified image
image.save('image_with_dialog.jpg')