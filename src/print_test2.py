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
        self.last_print_time_stamp = time.time()
        self.counter = 0
        
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
        
        #result = [[random.randint(0,1) for _ in range(300)] for _ in range(8)]

        return result

    def write_margin_text(self, img, counter, text_matrix):
        height = len(text_matrix)
        length = len(text_matrix[0])
        for i in range(height):
            if text_matrix[i][counter%length] == 1:
                img.putpixel((556 - i, 0), (0, 0, 0))
            if text_matrix[i][length - (counter%length) - 1] == 1:
                img.putpixel((i, 0), (0, 0, 0))

    def print_pixel_line(self, a_temp, b_temp, entanglement, broken_channel, text_matrix, counter):
        img = Image.new('RGB', (576, 1), "white")
        self.write_margin_text(img, counter, text_matrix)
        #Baseline
        img.putpixel((int(a_temp) + 273, 0), (0, 0, 0))
        img.putpixel((int(b_temp) + 273, 0), (0, 0, 0))
        img.putpixel((int(a_temp) + 273 + 1, 0), (0, 0, 0))
        img.putpixel((int(a_temp) + 273 - 1, 0), (0, 0, 0))
        img.putpixel((int(b_temp) + 273 + 1, 0), (0, 0, 0))  
        img.putpixel((int(b_temp) + 273 - 1, 0), (0, 0, 0)) 
        if entanglement:
            #DOUBLE SLIT

            #FIRST LINE 
            img.putpixel((int(a_temp) + 273 + 30, 0), (0, 0, 0))
            img.putpixel((int(a_temp) + 273 + 31, 0), (0, 0, 0))
            img.putpixel((int(a_temp) + 273 - 30, 0), (0, 0, 0))
            img.putpixel((int(a_temp) + 273 - 31, 0), (0, 0, 0))
            img.putpixel((int(b_temp) + 273 + 30, 0), (0, 0, 0))  
            img.putpixel((int(b_temp) + 273 + 31, 0), (0, 0, 0))  
            img.putpixel((int(b_temp) + 273 - 30, 0), (0, 0, 0)) 
            img.putpixel((int(b_temp) + 273 - 31, 0), (0, 0, 0)) 

            #THIRD LINE AND FORTH LINE
            img.putpixel((int(a_temp) + 273 + 60, 0), (0, 0, 0))
            img.putpixel((int(a_temp) + 273 + 90, 0), (100, 100, 100))
            img.putpixel((int(a_temp) + 273 - 60, 0), (0, 0, 0))
            img.putpixel((int(a_temp) + 273 - 90, 0), (100, 100, 100))
            img.putpixel((int(b_temp) + 273 + 60, 0), (0, 0, 0))  
            img.putpixel((int(b_temp) + 273 + 90, 0), (100, 100, 100))  
            img.putpixel((int(b_temp) + 273 - 60, 0), (0, 0, 0)) 
            img.putpixel((int(b_temp) + 273 - 90, 0), (100, 100, 100)) 

            #FIFTH LINE
            img.putpixel((int(a_temp) + 273 + 120, 0), (150, 150, 150))
            img.putpixel((int(b_temp) + 273 + 120, 0), (150, 150, 150))
            img.putpixel((int(a_temp) + 273 - 120, 0), (150, 150, 150))
            img.putpixel((int(b_temp) + 273 - 120, 0), (150, 150, 150))
        
        elif broken_channel:
            for t in range (576):
                if t>min(a_temp + 273, b_temp + 273) and t<=max(a_temp + 273, b_temp + 273):
                #if (min(a_temp + 273, b_temp + 273)-30)<t<min(a_temp + 273, b_temp + 273) or max(a_temp + 273, b_temp + 273)<t<(30 + max(a_temp + 273, b_temp + 273)):
                    img.putpixel((t, 0), (0, 0, 0))
                    #if img.getpixel((t, 0)) == (255, 255, 255):
                    #   img.putpixel((t, 0), (0, 0, 0))
                    #else:
                    #    img.putpixel((t, 0), (255, 255, 255))
        raster = StarTSPImage.imageToRaster(img, cut=False)
        printer = open('/dev/usb/lp0', "wb")
        printer.write(raster) 
        printer.close()

    def check_time_and_print(self, last_print_time_stamp, a_temp, b_temp, entanglement, broken_channel, text_matrix, counter):
        check_time = time.time()
        if check_time - last_print_time_stamp > 0:
            printer.print_pixel_line(a_temp, b_temp, entanglement, broken_channel, text_matrix, counter)
            printer.last_print_time_stamp = check_time
            self.counter = self.counter + 1

    def test(self):
        a_temp = 20
        b_temp = 40

        text_matrix = self.text_to_matrix(self.margin_text, self.font_height_5, self.text_scale)
        while True:
            time.sleep(0.1)
            if abs(a_temp - b_temp) > 25:
                self.check_time_and_print(self.last_print_time_stamp, a_temp, b_temp, False, True, text_matrix, self.counter)
                a_temp = min(max(0, a_temp + random.randint(-2, 2)), 50)
                b_temp = min(max(0, b_temp + random.randint(-2, 2)), 50)
            elif abs(a_temp - b_temp)<= 3:
                self.check_time_and_print(self.last_print_time_stamp, a_temp, b_temp, True, False, text_matrix, self.counter)
                a_temp = min(max(0, a_temp + random.randint(-2, 2)), 50)
                b_temp = min(max(0, b_temp + random.randint(-2, 2)), 50)
            else: 
                self.check_time_and_print(self.last_print_time_stamp, a_temp, b_temp, False, False, text_matrix, self.counter)
                a_temp = min(max(0, a_temp + random.randint(-2, 2)), 50)
                b_temp = min(max(0, b_temp + random.randint(-2, 2)), 50)


if __name__ == "__main__":
    printer = Printer()
    printer.test()