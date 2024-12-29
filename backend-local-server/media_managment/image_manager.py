import rembg
import os
import io
import cv2
import numpy as np
from PIL import Image
from graphics_engine import GraphicsEngine

class ImageManager:

    def __init__(self, output, frames_input):

        self.save_path = output
        self.frames = frames_input
        self.engine = GraphicsEngine(self.save_path)

    #   REMOVE BACKGROUND [DEFAULT]
    def remove_image_background(self, image_path, image_title):
        #   SAVE FOLDER 
        output_path = os.path.join(self.save_path, image_title)

        try:
            # Load the original image
            original_image = cv2.imread(image_path)

            # Step 1: Run preprocessing logic (edge detection and GrabCut)
            processed_image, dilated_edges = self.engine.run_canny_edge_detection(image_path)
            mask = np.zeros(processed_image.shape[:2], np.uint8)
            mask[dilated_edges > 0] = 1  # Use edges as a probable foreground

            # Refine mask with GrabCut
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            cv2.grabCut(processed_image, mask, None, bgd_model, fgd_model, iterCount=5, mode=cv2.GC_INIT_WITH_MASK)
            refined_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

            # Step 2: Pass the original image to rembg
            # Convert the original image to PIL format
            original_image_pil = Image.open(image_path)

            # Apply background removal with rembg
            array_input = np.array(original_image_pil)
            rembg_result = rembg.remove(array_input)

            # Convert rembg result to OpenCV format
            rembg_result_cv = cv2.cvtColor(np.array(Image.fromarray(rembg_result)), cv2.COLOR_RGBA2BGRA)

            # Step 3: Combine rembg mask with refined mask
            alpha_channel = rembg_result_cv[:, :, 3]  # Extract alpha channel from rembg
            combined_mask = cv2.bitwise_and(alpha_channel, refined_mask * 255)  # Combine masks

            # Apply the combined mask to the original image
            foreground = cv2.bitwise_and(original_image, original_image, mask=combined_mask)

            # Convert to PIL format for saving
            foreground_pil = Image.fromarray(cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB))

            # Save the final image
            foreground_pil.save(output_path)

            print(f"Background removed and saved to {output_path}")
        except Exception as error:
            print(f"Error removing background: {error}")

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

