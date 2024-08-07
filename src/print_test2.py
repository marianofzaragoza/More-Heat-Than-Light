import StarTSPImage
from PIL import Image, ImageDraw
import time
import random


FONT_height_5 = {
    'A': [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1]
    ],
    'B': [
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 0]
    ],
    'C': [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
    ],
    'D': [
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 0]
    ],
    'E': [
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 1]
    ],
    'F': [
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0]
    ],
    'G': [
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 1]
    ],
    'H': [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1]
    ],
    'I': [
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
    [1, 1, 1]
    ],
    'J': [
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
    ],
    'K': [
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 1]
    ],
    'L': [
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 1]
    ],
    'M': [
    [1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1]
    ],
    'N': [
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1]
    ],
    'O': [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
    ],
    'P': [
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0]
    ],
    'Q': [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
    ],
    'R': [
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1]
    ],
    'S': [
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 1, 0]
    ],
    'T': [
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
    ],
    'U': [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
    ],
    'V': [
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0]
    ],
    'W': [
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0]
    ],
    'X': [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1]
    ],
    'Y': [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0]
    ],
    'Z': [
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 1]
    ],
    ' ': [
    [1, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 1, 1]
    ],
    ' ': [
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0]
    ],

    }

def text_to_matrix(text, font, scale=1):
    # Determine the height of the font
    height = len(next(iter(font.values())))
    
    # Create an empty list to hold the result
    result = [[] for _ in range(height * scale)]
    
    for char in text:
        # Get the matrix for the current character, or use a space if character is not found
        char_matrix = font.get(char.upper(), font[' '])
        
        # Scale the character matrix
        scaled_matrix = []
        for row in char_matrix:
            scaled_row = []
            for pixel in row:
                scaled_row.extend([pixel] * scale)
            for _ in range(scale):
                scaled_matrix.append(scaled_row)
        
        # Append each row of the scaled character matrix to the result
        for i in range(height * scale):
            result[i].extend(scaled_matrix[i])
            result[i].extend([0] * scale)  # Add a space between characters scaled by scale
    
    # Remove the trailing space in each row
    for i in range(height * scale):
        result[i] = result[i][:-scale]
    
    return result

def sidetext(img, counter, text_matrix):
    height = len(text_matrix)
    length = len(text_matrix[0])
    for i in range(height):
        if text_matrix[i][counter%length] == 1:
            img.putpixel((height - i, 0), (0, 0, 0))
        if text_matrix[i][length - (counter%length) - 1]:
            img.putpixel((556 -height + i, 0), (0, 0, 0))

def print_pixel_line(a_temp, b_temp, ENTANGLEMENT, BROKEN_CHANNEL, text_matrix, counter):
    img = Image.new('RGB', (576, 1), "white")
    if ENTANGLEMENT:
        img.putpixel((int(a_temp) + 273, 0), (0, 0, 0))
        img.putpixel((int(b_temp) + 273, 0), (0, 0, 0))
    elif BROKEN_CHANNEL:
        for t in range (576):
            img.putpixel((int(a_temp) + 273, 0), (0, 0, 0))
            img.putpixel((int(b_temp) + 273, 0), (0, 0, 0))
    else:
        img.putpixel((int(a_temp) + 273, 0), (0, 0, 0))
        img.putpixel((int(b_temp) + 273, 0), (0, 0, 0))
    sidetext(img, counter, text_matrix)
    raster = StarTSPImage.imageToRaster(img, cut=False)
    printer = open('/dev/usb/lp0', "wb")
    printer.write(raster) 
    printer.close()


scale = 2
a_temp = 20
b_temp = 45
text = "ALICE AND BOB AND "

counter = 0
text_matrix = text_to_matrix(text, FONT_height_5, scale)
for i in range(2000):
    if abs(a_temp - b_temp) > 30:
        print_pixel_line(a_temp, b_temp, False, False, text_matrix, counter)
    else: 
        print_pixel_line(a_temp, b_temp, False, True, text_matrix, counter)
    counter = counter + 1
    a_temp = min(max(0, a_temp + random.randint(-2, 2)), 50)
    b_temp = min(max(0, b_temp + random.randint(-2, 2)), 50)
