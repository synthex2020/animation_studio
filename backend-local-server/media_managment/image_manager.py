import rembg
import os
import io
import numpy as np
from PIL import Image

class ImageManager:

    def __init__(self, output, frames_input):

        self.save_path = output
        self.frames = frames_input

    #   REMOVE BACKGROUND [DEFAULT]
    def remove_image_background(self, image_path, image_title):
        #   SAVE FOLDER 
        output_path = os.path.join(self.save_path, image_title)

        #   LOAD THE INPUT IMAGE 
        image_input = Image.open(image_path)

        #   CONVERTING INPUT TO NUMPY ARRAY 
        array_input = np.array(image_input)

        #   APPLYING BACKGROUND REMOVAL WITH REMBG
        resultant_image = rembg.remove(array_input)

        #   CREATE A PIL IMAGE FROM ARRAY OUTPUT 
        image_output = Image.fromarray(resultant_image)

        #   SAVE THE IMAGE 
        image_output.save(output_path)

    #   ADD BACKGROUND TO IMAGES [DEFAULT] - uses frames input as input 
    def add_new_background(self, new_background):
        #   LOADING THE PATHS 
        images = self.frames

        #   LOAD NEW BACKGROUND 
        background = Image.open(new_background).convert("RGBA")
        count = 1
        #   BATCH PROCESSING IMAGES 
        for filename in os.listdir(images):
            #   ONLY PROCESSING PNG FILES 
            if filename.endswith('.png'):
                input_path = os.path.join(images, filename)
                output_path = os.path.join(self.save_path, filename)

                #   READ AND PROCESS THE IMAGE 
                with open(input_path, 'rb') as file:
                    input_image = file.read()
                    output_image = rembg.remove(input_image)

                #   CONVERT RESULT INTO PIL IMAGE 
                subject_image = Image.open(io.BytesIO(output_image)).convert("RGBA")

                #   RESIZE THE BACKGROUND TO MATCH THE SIZE OF THE IMAGE 
                resized_background = background.resize(subject_image.size)

                #   COMPOSITE THE SUBJECT IMAGE OVER THE BACKGROUND 
                final_image = Image.alpha_composite(resized_background, subject_image)

                #   SAVE THE RESULT 
                final_image.save(output_path) 

                print(f"\rProccessed {filename} --> {count}", end='')
                count += 1
        print("Processing complete")      


    #   UPLOAD IMAGES TO SOME URL 

    #   DOWNLOAD IMAGES TO SOME URL 

