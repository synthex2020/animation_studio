import cv2
import os 
import sys
from glob import glob
from PIL import Image
from pathlib import Path 



class VideoManager: 

    #  """
    #    Initialize the VideoRendering class.
    #
    #    :param source_path: Path where the frames are stored.
    #    :param saved_path: Path where the video will be saved.
    #    :param title: Name of the output video file.
    #    :param fps: Frames per second for the output video.
    #    """

    def __init__(self, working_dir, frames_path, title, saved_path):
        self.working_dir = working_dir
        self.mean_height = 0
        self.mean_width = 0
        self.source_path = frames_path
        self.result_title = title
        self.saved_path = saved_path
        self.number_images = len(
            [f for f in os.listdir(self.source_path) if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")]
        )
        self.fps = 30

    #   UPDATE SOURCE PATH 
    def update_source(self, new_path):
        self.source_path = new_path

    #   BREAK VIDEO INTO FRAMES 
    def break_into_frames(self, video_file):
        #   PATH TO VIDEO FILE 
        video_object = cv2.VideoCapture(video_file)
        
        #   FIND FPS 
        self.fps = video_object.get(cv2.CAP_PROP_FPS)
        #   COUNTER VARIABLE 
        count = 0 ; 

        #   CHECK IF FRAMES WERE EXTRACTED 
        success = 1

        #   VIDEO OBJECT CALLS READ TO EXTRACT 
        # 
        #  
        success, image = video_object.read()
        
        while success:
            #   SAVE THE FRAMES WITH RELEVANT COUNT 
            if image is not None:
                cv2.imwrite(f'{self.working_dir}\\backend-local-server\\generation_output\\frames\\{count}.png', image)
                count += 1
            #   READ THE NEXT FRAME 
            success, image = video_object.read()
        
        #   UPDATE THE LIST OF IMAGES PROPERTY 
        self.number_images = count
        
        #   FREE UP RESOURCES 
        video_object.release()

    #   PUT FRAMES TOGETHER INTO VIDEO 
    def render_frames_to_video(self):
        """
        Convert the images in the source path into a video.
        """
        images = sorted(
            [img for img in os.listdir(self.source_path) if img.endswith(".png") or img.endswith(".jpg") or img.endswith(".jpeg")],
            key=lambda x: int(os.path.splitext(x)[0])  # Assumes filenames are numeric
        )

        if not images:
            print("No valid frames found in the source path.")
            return

        # Determine frame dimensions
        frame = cv2.imread(os.path.join(self.source_path, images[0]))
        height, width, layers = frame.shape

        # Define the VideoWriter
        output_path = os.path.join(self.saved_path, self.result_title)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
        video_result = cv2.VideoWriter(output_path, fourcc, self.fps, (width, height))

        # Render frames into the video
        for i, image in enumerate(images):
            frame = cv2.imread(os.path.join(self.source_path, image))
            if frame is None:
                print(f"Warning: Frame {image} could not be read and will be skipped.")
                continue
            video_result.write(frame)

            # Display progress
            progress = (i + 1) / len(images)
            hashes = "#" * int(progress * 30)
            spaces = " " * (30 - len(hashes))
            sys.stdout.write(f"\rProgress: [{hashes}{spaces}] {progress * 100:.2f}%")
            sys.stdout.flush()

        # Release VideoWriter
        video_result.release()
        cv2.destroyAllWindows()
        print(f"\nVideo saved to {output_path}")


    #   Resize all images in the source path to have uniform dimensions based on the mean dimensions.
    def equalize_dimensions(self):

        for file in os.listdir(self.source_path):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
                im = Image.open(os.path.join(self.source_path, file))
                width, height = im.size
                self.mean_width += width
                self.mean_height += height
        self.mean_width = int(self.mean_width / self.number_images)
        self.mean_height = int(self.mean_height / self.number_images)

        # Resizing images
        for file in os.listdir(self.source_path):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
                im = Image.open(os.path.join(self.source_path, file))
                im_resize = im.resize((self.mean_width, self.mean_height), Image.LANCZOS)
                im_resize.save(os.path.join(self.source_path, file), 'PNG', quality=95)   

    #   Move the video to the save folder and clean up intermediate files.
    def garbage_collection(self):
        """
        Move the video to the save folder and clean up intermediate files.
        """
        current_path_result = os.path.join(os.getcwd(), self.result_title)
        destination_path_result = os.path.join(self.saved_path, self.result_title)
        
        #   CHECK IF THE OUTPUT IS IN THE RIGHT PLACE 
        if not destination_path_result.__contains__('\\video\\'):
            Path(current_path_result).rename(destination_path_result)

        # Delete the intermediate frame images
        frame_files = glob(os.path.join(self.source_path, "*.png"))
        for frame in frame_files:
            os.remove(frame)

    #   UPSCALE VIDEO QUALITY 



