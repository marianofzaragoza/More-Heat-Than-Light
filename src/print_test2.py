import StarTSPImage
from PIL import Image, ImageDraw
import time
import random
from config import DynamicConfigIni

class Printer():
    def __init__(self):
        self.config = DynamicConfigIni()
        self.text_scale = int(self.config.printer.text_scale)
        self.margin_text = self.config.printer.margin_text
        
        
    font_height_5 = {
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
        '&': [
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

    def text_to_matrix(self, text, font, scale):
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

    def write_margin_text(self, img, counter, text_matrix):
        height = len(text_matrix)
        length = len(text_matrix[0])
        for i in range(height):
            if text_matrix[i][counter%length] == 1:
                img.putpixel((height - i, 0), (0, 0, 0))
            if text_matrix[i][length - (counter%length) - 1]:
                img.putpixel((556 -height + i, 0), (0, 0, 0))

    def print_pixel_line(self, a_temp, b_temp, ENTANGLEMENT, BROKEN_CHANNEL, text_matrix, counter):
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
        self.write_margin_text(img, counter, text_matrix)
        raster = StarTSPImage.imageToRaster(img, cut=False)
        printer = open('/dev/usb/lp0', "wb")
        printer.write(raster) 
        printer.close()

    def test(self):
        a_temp = 20
        b_temp = 45

        counter = 0
        text_matrix = self.text_to_matrix(self.margin_text, self.font_height_5, self.text_scale)

        for i in range(2000):
            if abs(a_temp - b_temp) > 30:
                self.print_pixel_line(a_temp, b_temp, False, False, text_matrix, counter)
            else: 
                self.print_pixel_line(a_temp, b_temp, False, True, text_matrix, counter)
            counter = counter + 1
            a_temp = min(max(0, a_temp + random.randint(-2, 2)), 50)
            b_temp = min(max(0, b_temp + random.randint(-2, 2)), 50)




if __name__ == "__main__":
    printer = Printer()
    printer.test()
