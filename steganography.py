from PIL import Image

# Function to convert data into 8-bit binary form using ASCII values of characters
def genData(data):
    # List of binary codes of given data
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Function to modify pixels according to the 8-bit binary data and yield modified pixel tuples
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in next(imdata)[:3] +
               next(imdata)[:3] +
               next(imdata)[:3]]

        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # Eighth pixel of every set tells whether to stop or read further.
        # 0 means keep reading; 1 means the message is over.
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                pix[-1] -= 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

# Function to encode data into image
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

# Function to encode data into image
def encode():
    img = input("Enter image name (with extension): ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded: ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image (with extension): ")
    newimg.save(new_img_name)
    print(f"Encoded image saved as {new_img_name}")

# Function to decode data from image
def decode():
    img = input("Enter image name (with extension): ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in next(imgdata)[:3] +
                  next(imgdata)[:3] +
                  next(imgdata)[:3]]

        # String of binary data
        binstr = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        # Convert binary string to character and append to data
        data += chr(int(binstr, 2))

        # Check for end of message indicator
        if pixels[-1] % 2 != 0:
            break

    print("Decoded message:", data)

# Main function to choose between encoding and decoding
def main():
    while True:
        print(":: Welcome to Steganography ::")
        print("1. Encode")
        print("2. Decode")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            encode()
        elif choice == '2':
            decode()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
