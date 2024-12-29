import cv2
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw


class ImageProcessing: 

    def __init__(self, working_dir):
        self.working_dir = working_dir

    
    #   ENHANCE CONTRAST AND SHARPNESS 
    def enhance_image(self, gray):
        #   Apply CLAHE for contrast enhancement 
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        #   Apply sharpening filter 
        sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0, -1, 0]])
        sharpened = cv2.filter2D(enhanced, -1, sharpen_kernel)

        return sharpened
    
    #   RUN MULTI-SELECT EDGE DETECTION 
    def multi_scale_edge_detection(self, image):
        #   Perform edge detection at original scale 
        large_edges = cv2.Canny(image, threshold1=50, threshold2=150)

        #   Downscale and detect edges 
        small = cv2.resize(image, None, fx=0.5, fy=0.5)
        small_edges = cv2.Canny(small, threshold1=50, threshold2=150)
        small_edges = cv2.resize(small_edges, image.shape[::-1])

        #   Combine multi-scale edges 
        merged_edges = cv2.bitwise_or(large_edges, small_edges)
        return merged_edges

    #   RUN CANNY EDGE DETECTION 
    def run_canny_edge_detection(self, image_path):
        try:
            #   Load file paths 
            processing_output = self.working_dir
            image_input = image_path

            #   Load the original image 
            image = cv2.imread(image_input)

            #   Convert to grayscale for edge detection 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            #   Enhance image ( constrast and sharpness )
            enhanced = self.enhance_image(gray)

            #   Apply Gaussian Blur to reduce noise 
            blurred = cv2.GaussianBlur(enhanced, (5,5),0)

            #   Perfom multi-scale edge detection 
            edges = self.multi_scale_edge_detection(blurred)

            #   Fill in the gaps with morphological closing 
            kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernal)

            #   Dilate edges to create a rough mask 
            dilated_egdes = cv2.dilate(closed_edges, kernal, iterations=1)

            #   Display results 
            #plt.imshow(dilated_egdes, cmap='gray')
            #plt.title('Dilated Edges for Preproessing')
            #plt.show()

            return (image, dilated_egdes)

        except Exception as error:
            print(error)

    #   RUN GRAB CUT EDGE MASK CREATION 
    def run_grab_cut_edge_mask_creation(self, image_input, diluted_edges):
        try:
            #   Load file paths 
            processing_output = self.working_dir
            input_image = image_input

            #   Create initial mask 
            mask = np.zeros(image_input.shape[:2], np.uint8)

            #   Use diluted edges to define probable foreground 
            mask[diluted_edges > 0] = 1 

            #   Define the models 
            bgd_model = np.zeros((1,65), np.float64)
            fgd_model = np.zeros((1,65), np.float64)

            #   Apply Grab Cut 
            cv2.grabCut(image_input, mask, None, bgd_model, fgd_model, iterCount=5, mode=cv2.GC_INIT_WITH_MASK)

            #   Convert grab cut result into binary mask 
            final_mask = np.where((mask ==2) | (mask == 0), 0, 1).astype('uint8')

            #   Apply the mask to the image 
            foreground = image_input * final_mask[:, :, np.newaxis]

            #   Display results
            #plt.imshow(cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB))
            #plt.title('Background exractaed with GrabCut')
            #plt.show()

        except Exception as error:
            print(error)

    #   OPTIMIZE FOR EXTRACTION 
    def optimize_for_extraction(self, target):
        try:
            #   Load file path 
            processing_output = self.working_dir

            #   RUN EDGE DETECTION 
            canny_result =  self.run_canny_edge_detection(target)
            #   RUN GRAB CUT 
            self.run_grab_cut_edge_mask_creation(canny_result[0], canny_result[1])

        except Exception as error:
            print(error)

    #   PLOTTING ANATOMY MODELS 
    def detect_and_plot_lines(self, processed_image, output_canvas_size=(512, 512)):
        try:
            # Convert to grayscale if not already
            gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)

            # Apply Canny Edge Detection (if edges aren't detected yet)
            edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

            # Detect lines using Hough Transform
            lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

            # Prepare a blank canvas for plotting
            canvas = Image.new('RGB', output_canvas_size, color='white')
            draw = ImageDraw.Draw(canvas)

            # If lines are detected, draw them on the canvas
            if lines is not None:
                for line in lines:
                    rho, theta = line[0]
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                    # Scale coordinates to fit canvas size
                    x1, y1 = self.scale_to_canvas((x1, y1), processed_image.shape, output_canvas_size)
                    x2, y2 = self.scale_to_canvas((x2, y2), processed_image.shape, output_canvas_size)

                    # Draw the line on the canvas
                    draw.line((x1, y1, x2, y2), fill='black', width=2)

            # Display the resulting construction model
            plt.imshow(canvas)
            plt.axis('off')
            plt.title('Construction Model')
            plt.show()

            return canvas

        except Exception as error:
            print(f"Error in detect_and_plot_lines: {error}")

    def scale_to_canvas(self, coord, original_size, canvas_size):
        """
        Scales coordinates from the original image size to the canvas size.
        """
        x, y = coord
        orig_h, orig_w = original_size[:2]
        canvas_w, canvas_h = canvas_size
        scaled_x = int(x * canvas_w / orig_w)
        scaled_y = int(y * canvas_h / orig_h)
        return scaled_x, scaled_y

    def run_plot_detection(self, image_path):
        processed = cv2.imread(image_path)
        canvas = self.detect_and_plot_lines(processed)


