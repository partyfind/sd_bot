from PIL import Image, ImageDraw, ImageFont

# Set up constants for dialog box and text color
DIALOG_BOX_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
NAME_COLOR = (255, 0, 0)
DIALOG_BOX_SIZE_PERCENT = 0.05
FONT_SIZE = 12

# Open the image and get its dimensions
image = Image.open("image.jpg")
image_width, image_height = image.size

# Open the dialog file and read the lines
with open("dialogs.txt", "r") as f:
    dialog_lines = f.readlines()

# Calculate the size of the dialog box based on the image size
dialog_box_size = int(DIALOG_BOX_SIZE_PERCENT * min(image_width, image_height))

# Set up the font for the dialog box
font = ImageFont.truetype("arial.ttf", FONT_SIZE)

# Iterate through each dialog line in the file
for dialog_line in dialog_lines:
    # Split the dialog line into the character name and the dialog text
    character, dialog_text = dialog_line.strip().split(": ")
    character = character.strip()
    dialog_text = dialog_text.strip()

    # Calculate the position of the dialog box based on the image size and character name length
    name_length = len(character)
    dialog_box_x = int((image_width - dialog_box_size * (name_length + 1)) / 2)
    dialog_box_y = int(image_height * 0.8)

    # Create a new image for the dialog box
    dialog_box_image = Image.new("RGB", (dialog_box_size * (name_length + 1), dialog_box_size), DIALOG_BOX_COLOR)

    # Draw the character name on the dialog box
    draw = ImageDraw.Draw(dialog_box_image)
    draw.text((0, 0), character + ":", font=font, fill=NAME_COLOR)

    # Draw the dialog text on the dialog box
    draw.text((dialog_box_size, 0), dialog_text, font=font, fill=TEXT_COLOR)

    # Draw the oval shape around the dialog box
    oval_width = dialog_box_size * (name_length + 1)
    oval_height = dialog_box_size
    oval_left = dialog_box_x
    oval_top = dialog_box_y - oval_height
    oval_right = oval_left + oval_width
    oval_bottom = oval_top + oval_height
    draw.ellipse((oval_left, oval_top, oval_right, oval_bottom), outline=TEXT_COLOR)

    # Paste the dialog box image onto the original image
    image.paste(dialog_box_image, (dialog_box_x, dialog_box_y))

# Save the new image with dialog boxes
image.save("image_with_dialogs.jpg")
