# Скрипт объединяет 10 картинок в одну
from PIL import Image, ImageDraw
import os

num_rows = 2
num_cols = 5
cell_width = 500
cell_height = 300
border_width = 2  # adjust as needed
table_width = num_cols * cell_width + (num_cols + 1) * border_width
table_height = num_rows * cell_height + (num_rows + 1) * border_width
table_img = Image.new(mode='RGB', size=(table_width, table_height))
draw = ImageDraw.Draw(table_img)

img_dir = './img'
img_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith('.png')]

for i, img_file in enumerate(img_files):
    img = Image.open(img_file)
    img = img.resize((cell_width, cell_height))
    row = i // num_cols
    col = i % num_cols
    x = col * cell_width + (col+1) * border_width
    y = row * cell_height + (row+1) * border_width
    draw.rectangle((x, y, x+cell_width, y+cell_height), outline='white', width=border_width)
    table_img.paste(img, (x+border_width, y+border_width))

table_img.save('img/merged_table.jpg')


#альтернативный
"""from PIL import Image

# Define the number of rows and columns
ROWS = 2
COLS = 5

# Define the size of each individual image
WIDTH = 500
HEIGHT = 200

# Open and resize the images
images = []
for i in range(1, 11):
    img = Image.open(f"img/{i}.png")
    img = img.resize((WIDTH, HEIGHT))
    images.append(img)

# Create a new image for the merged table
merged_img = Image.new('RGB', (WIDTH*COLS, HEIGHT*ROWS), color='white')

# Paste the individual images into the merged image
for row in range(ROWS):
    for col in range(COLS):
        index = row*COLS + col
        if index < len(images):
            x = col*WIDTH
            y = row*HEIGHT
            merged_img.paste(images[index], (x, y))

# Save the merged image
merged_img.save("img/merged.jpg")"""