from PIL import Image

def hide_text_in_image(image_path, text):
    # Open the image file
    img = Image.open(image_path)
    
    # Convert the text to binary
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    
    # Check if the binary text can fit in the image
    if len(binary_text) > img.width * img.height * 3:
        raise ValueError("Text too long to hide in image.")
    
    # Iterate over each pixel in the image
    pixel_index = 0
    for y in range(img.height):
        for x in range(img.width):
            # Get the current pixel
            pixel = img.getpixel((x, y))
            
            # Convert the pixel to a list of RGB values
            pixel_rgb = list(pixel)
            
            # Iterate over each RGB value in the pixel
            for i in range(3):
                # Check if there are more bits to hide
                if pixel_index < len(binary_text):
                    # Get the current bit to hide
                    bit_to_hide = int(binary_text[pixel_index])
                    
                    # Replace the least significant bit of the RGB value with the bit to hide
                    pixel_rgb[i] = (pixel_rgb[i] & ~1) | bit_to_hide
                    
                    # Increment the pixel index
                    pixel_index += 1
            
            # Update the pixel with the new RGB values
            img.putpixel((x, y), tuple(pixel_rgb))
    
    # Save the image with the hidden text
    img.save("hidden_text.png")

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Iterate over each pixel in the image
    binary_text = ""
    for y in range(img.height):
        for x in range(img.width):
            # Get the current pixel
            pixel = img.getpixel((x, y))
            
            # Convert the pixel to a list of RGB values
            pixel_rgb = list(pixel)
            
            # Iterate over each RGB value in the pixel
            for i in range(3):
                # Get the least significant bit of the RGB value
                bit = pixel_rgb[i] & 1
                
                # Add the bit to the binary text
                binary_text += str(bit)
    
    # Convert the binary text to ASCII
    text = ""
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        text += chr(int(byte, 2))
    
    return text

# method calls
hide_text_in_image("my_image.png", "This is some hidden text.")

# extract text
text = extract_text_from_image("hidden_text.png")
print(text)
