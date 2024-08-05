import StarTSPImage
from PIL import Image, ImageDraw
import time

from PIL import Image, ImageDraw
import random

# Define the 3x3 pixel font for each character
FONT_3X3 = {
    'A': [
        [0, 1, 0],
        [1, 1, 1],
        [1, 0, 1]
    ],
    'B': [
        [1, 1, 0],
        [1, 1, 1],
        [1, 1, 0]
    ],
    'C': [
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1]
    ],
    'D': [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 0]
    ],
    'E': [
        [1, 1, 1],
        [1, 1, 0],
        [1, 1, 1]
    ],
    'F': [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 0]
    ],
    'G': [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1]
    ],
    'H': [
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1]
    ],
    'I': [
        [1, 1, 1],
        [0, 1, 0],
        [1, 1, 1]
    ],
    'J': [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 0]
    ],
    'K': [
        [1, 0, 1],
        [1, 1, 0],
        [1, 0, 1]
    ],
    'L': [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ],
    'M': [
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1]
    ],
    'N': [
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1]
    ],
    'O': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    'P': [
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 0]
    ],
    'Q': [
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 1]
    ],
    'R': [
        [1, 1, 0],
        [1, 1, 1],
        [1, 0, 1]
    ],
    'S': [
        [0, 1, 1],
        [0, 1, 0],
        [1, 1, 0]
    ],
    'T': [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    'U': [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    'V': [
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1]
    ],
    'W': [
        [1, 0, 1],
        [1, 1, 1],
        [1, 1, 1]
    ],
    'X': [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ],
    'Y': [
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    'Z': [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ],
    ' ': [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
}

def render_text_to_pixels(text, max_width):
    # Calculate character width including spacing (3 pixels per character + 1 pixel space)
    char_width = 4
    max_chars = max_width // char_width

    # Convert text to pixel representation
    rows = [[] for _ in range(3)]
    for char in text[:max_chars]:  # Only process up to the maximum number of characters that fit
        if char in FONT_3X3:
            char_pixels = FONT_3X3[char]
            for i in range(3):
                rows[i].extend(char_pixels[i])
                rows[i].append(0)  # Add a space between characters
        else:
            # Handle unknown characters
            for i in range(3):
                rows[i].extend([0, 0, 0])
                rows[i].append(0)  # Add a space between characters
    return rows

def create_image_from_pixels(pixels, max_width, scale=1):
    # Determine the size of the image
    
    height = len(pixels) * scale
    
    # Limit width to max_width
    width = 576
    
    # Create a new image with white background
    img = Image.new('RGB', (width, height + 1*scale), "white")
    draw = ImageDraw.Draw(img)

    # Draw the pixels
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            if pixel == 1 and (x * scale) < max_width:
                draw.rectangle([x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1], fill="black")

    return img

def create_vertical_image_from_pixels(pixels, offset):
    width = 576
    height = 5000

    # Create a new image with a white background
    img = Image.new('RGB', (width, height), "white")

    # Draw the pixels vertically along the left margin
    for col in range(len(pixels[0])):  # Iterate over each character
        for row in range(len(pixels)):  # Iterate over the rows of the character (0 to 2)
            if pixels[row][col] == 1:  # Check if the pixel is "on"
                # Draw the pixel at (0, y + col)
                if (row + col) < height:  # Ensure within image bounds
                    a = 0 #img.putpixel((offset + 3 - row, col), (0, 0, 0)) #left hand side
                    #img.putpixel((width - 1 - offset - row, col), (0, 0, 0)) # right hand side

    return img




# Example usage
vertical_text = ""
max_width = 5000
pixels = render_text_to_pixels(vertical_text, max_width)
#img = create_image_from_pixels(pixels, max_width)
img = create_vertical_image_from_pixels(pixels, 5)
a_temp= 270
b_temp= 278
entanglement = "                                                                  ENTANGLEMENT                                                                  "
i = 0
a_temp= 270
b_temp= 290
entanglement = "                                                                  ENTANGLEMENT                                                                  "
broken_channel = "   BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN CHANNEL BROKEN"
i = 0
while i < 5000:
    if 30 > abs(a_temp - b_temp)> 0:
        img.putpixel((a_temp, i), (0, 0, 0))
        img.putpixel((a_temp + 1, i), (0, 0, 0))
        img.putpixel((a_temp - 1, i), (0, 0, 0))
        img.putpixel((b_temp, i), (0, 0, 0))
        img.putpixel((b_temp + 1, i), (0, 0, 0))
        img.putpixel((b_temp - 1, i), (0, 0, 0))
        a_temp = min(max(273, a_temp + random.randint(-2, 2)), 323)
        b_temp = min(max(273, b_temp + random.randint(-2, 2)), 323)
        i = i + 1
    elif 30 <= abs(a_temp - b_temp):
        for t in range(576):
            if t < min(a_temp, b_temp) or t > max(a_temp, b_temp):
                img.putpixel((t, i), (256, 256, 256))
        a_temp = min(max(273, a_temp + random.randint(-2, 2)), 323)
        b_temp = min(max(273, b_temp + random.randint(-2, 2)), 323)
        i = i + 1
    else:
        pixels = render_text_to_pixels(entanglement, 576)
        for y, row in enumerate(pixels):
            for x, pixel in enumerate(row):
                if pixel == 1 and (x) < max_width and y + i < max_width:
                    img.putpixel((x, y + i), (0, 0, 0))
        for t in range (4):
            a_temp = min(max(273, a_temp + random.randint(-2, 2)), 323)
            b_temp = min(max(273, b_temp + random.randint(-2, 2)), 323)
        i = i + 4


#image = Image.new('RGB', (500, 1000), "white")
#draw = ImageDraw.Draw(image)
#for i in range (500):
#    for j in range (1000):
#        if i%2 == 0 and j%2 == 0:
#             image.putpixel((i, j), (0, 0, 0))
       

raster = StarTSPImage.imageToRaster(img, cut=False)
printer = open('/dev/usb/lp0', "wb")
printer.write(raster) 
printer.close()

