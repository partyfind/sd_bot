from PIL import Image, ImageDraw, ImageFont

# Define constants
FONT_SIZE = 30
CLOUD_SIZE_PERCENT = 0.05
TEXT_PADDING = 20
TEXT_COLOR = (0, 0, 0)
CLOUD_COLOR = (255, 255, 255)
CHARACTER_COLOR = (255, 0, 0)

# Open the image file
img = Image.open("image.jpg")

# Calculate the size of the dialog cloud based on the image size
cloud_size = int(min(img.size) * CLOUD_SIZE_PERCENT)

# Load the font
font = ImageFont.truetype("font.ttf", FONT_SIZE)

# Open the dialog file
with open("dialogs.txt", "r") as f:
    # Loop over each line in the file
    for line in f:
        # Split the line into the character and the dialog
        character, dialog = line.strip().split(": ")

        # Calculate the size of the text
        text_size = font.getsize(dialog)

        # Calculate the position of the dialog cloud
        if "left" in character.lower():
            x = cloud_size
        elif "right" in character.lower():
            x = img.size[0] - cloud_size - text_size[0] - TEXT_PADDING * 2
        else:
            x = cloud_size
        y = min(img.size[1] - cloud_size - text_size[1] - TEXT_PADDING * 2, max(cloud_size, img.size[1] / 2 - text_size[1]))

        # Create a new image for the dialog cloud
        cloud = Image.new("RGBA", (cloud_size + text_size[0] + TEXT_PADDING * 2, cloud_size + text_size[1] + TEXT_PADDING * 2))

        # Draw the dialog cloud
        draw = ImageDraw.Draw(cloud)
        draw.ellipse((0, 0, cloud_size, cloud_size), fill=CLOUD_COLOR)
        draw.rectangle((cloud_size / 2, 0, cloud_size + text_size[0] + TEXT_PADDING * 2, text_size[1] + TEXT_PADDING * 2), fill=CLOUD_COLOR)
        draw.rectangle((0, cloud_size / 2, cloud_size + text_size[0] + TEXT_PADDING * 2, cloud_size + text_size[1] + TEXT_PADDING * 2), fill=CLOUD_COLOR)
        draw.text((cloud_size / 2 + TEXT_PADDING, TEXT_PADDING), dialog, fill=TEXT_COLOR, font=font)

        # Paste the dialog cloud onto the image
        img.paste(cloud, (int(x), int(y)), mask=cloud)

        # Draw the character name
        draw = ImageDraw.Draw(img)
        draw.text((x - TEXT_PADDING, y - FONT_SIZE), character, fill=CHARACTER_COLOR, font=font)

# Save the modified image
img.save("example_dialogs.jpg")
