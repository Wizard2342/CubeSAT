import time

import bluetooth
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import os
import time

def FileSave(imagepath):
    f = open(imagepath, "rb")
    data = f.read()
    decoded_data = base64.b64decode(data)
    #print(decoded_data)
    image = Image.open(BytesIO(decoded_data))
    filename_to_save = imagepath.split(".")
    image.save(filename_to_save[0]+".jpeg","JPEG")
    return filename_to_save[0]+".jpeg"

def convert_to_8bit_grayscale(img, index):
    # Read the image
    image = cv2.imread(img)

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image to 8-bit
    eight_bit_image = cv2.convertScaleAbs(grayscale_image)

    # Generate a unique filename based on timestamp with milliseconds and index
    timestamp = time.strftime("%Y%m%d_%H%M%S_%f")
    filename = f"grayscale_image_{index}_{timestamp}.jpg"

    # Save the grayscale image
    cv2.imwrite(filename, eight_bit_image)

    return filename
def divide_image_into_sections(image, num_sections):
    # Read the grayscale image
    grayscale_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    # Get image dimensions
    height, width = grayscale_image.shape[:2]

    # Calculate section dimensions
    section_height = height // num_sections
    section_width = width // num_sections

    sections = []
    section_locations = []

    for i in range(num_sections):
        for j in range(num_sections):
            # Calculate section boundaries
            top = i * section_height
            bottom = (i + 1) * section_height
            left = j * section_width
            right = (j + 1) * section_width

            # Extract section from the image
            section = grayscale_image[top:bottom, left:right]
            sections.append(section)

            # Store section locations for drawing text
            section_locations.append((left, top))

    return sections, section_locations

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)
import cv2
import numpy as np
str_length = ""
images_received_list = []
try:
    filenum = 0
    while True:
        i = 0
        total_length = 0
        length_baseline = ""
        data = client_sock.recv(1024)
        str_length = data.decode("utf-8")


        if str_length == "Sending Image:":
            filenum = filenum + 1
            filename = "received_data_" + str(filenum) + ".bin"
            f = open(filename, "wb")
            #length = client_sock.recv(1024)
            data = client_sock.recv(1024)
            str_length = data.decode("utf-8")
            print(str_length)
            length_baseline = str_length
            time.sleep(5)
            #data = client_sock.recv(1024)
            #str_length = data.decode("utf-8")
            #print(str_length)
            second_latest_image_path = ""
            latest_image_path = ""
            data = ""
            #length_baseline = str_length
            total_length = 0
            i = 0
            time.sleep(5)
            while True:
                data_image = client_sock.recv(1024)
                print(str(len(data_image)))
                i = len(data_image)
                total_length = i + total_length
                #data = client_sock.recv(2048)
                #print(str(len(data)))
                #i = len(data)
                #total_length = i+total_length
                #i = i + 1
                #if not data:
                #    break
                #print("Received", data)
                #decoded_data = base64.b64decode(data)
                f.write(data_image)
                if length_baseline != "":
                    if total_length == int(length_baseline):
                        f.close()

                        jpeg_file_name = FileSave(filename)
                        print("Image Saved as jpeg")
                        if len(images_received_list) > 1:
                            second_latest_image_path = images_received_list[-1]
                            latest_image_path = jpeg_file_name
                        images_received_list.append(jpeg_file_name)



                        if (latest_image_path != "") and (second_latest_image_path != ""):  # Check if paths are valid
                            # Convert images to grayscale and save them
                            grayscale_image1_path = convert_to_8bit_grayscale(latest_image_path, 1)
                            grayscale_image2_path = convert_to_8bit_grayscale(second_latest_image_path, 2)
                            #grayscale_image1_path = latest_image_path
                            #grayscale_image2_path = second_latest_image_path
                            # Divide the images into sections
                            num_sections = 12
                            sections_image1, _ = divide_image_into_sections(grayscale_image1_path, num_sections)
                            sections_image2, section_locations = divide_image_into_sections(grayscale_image2_path,
                                                                                            num_sections)

                            # Calculate the difference between the average pixel values for each section
                            difference_values = [abs(np.mean(section1) - np.mean(section2)) for section1, section2 in
                                                 zip(sections_image1, sections_image2)]

                            # Create a blank image with the same size as the original images
                            image1 = cv2.imread(latest_image_path)
                            overlay = np.zeros_like(image1)

                            # Overlay the difference values on the blank image
                            for i, diff in enumerate(difference_values):
                                x, y = section_locations[i]
                                cv2.putText(overlay, f"{diff:.2f}", (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (255, 255, 255), 2)

                            # Blend the overlay with the original image
                            alpha = 0.5  # Overlay transparency
                            result = cv2.addWeighted(image1, alpha, overlay, 1 - alpha, 0)

                            # Display the result
                            cv2.imwrite("Image1.jpeg",result)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                        else:
                            print("Error: No valid image paths found.")
                        break


                    #print(str(i))
                    #cv2.imshow("Image",data)

    #f.close()
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()

print("All done.")