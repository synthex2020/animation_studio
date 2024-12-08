from media_managment.video_manager import VideoManager
from media_managment.image_manager import ImageManager


class MediaManager:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.video_manager = None
        self.image_manager = None
        self.title = None
        self.source_path = None
        

    #   INITIALIZE THE VIDEO MANAGER 
    def init_video_manager(self, title, frames, output):
        #   INIT MANAGER 
        self.video_manager = VideoManager(
            working_dir=self.working_dir,
            frames_path=frames, 
            saved_path=output, 
            title=title 
            )
        

    #   INITALIZE THE IMAGE MANAGER 
    def init_image_manager(self, output_folder, frames_input_folder):
        self.image_manager = ImageManager(frames_input=frames_input_folder, output=output_folder)

    def update_source(self, new_path):
        self.video_manager.update_source(new_path)
    
    def break_into_frames(self, video_file):
        self.video_manager.break_into_frames(video_file=video_file)

    def render_frames_to_video(self):
        self.video_manager.render_frames_to_video()

    def garbage_collection(self):
        self.video_manager.garbage_collection()

    def equalize_dimensions(self):
        self.video_manager.equalize_dimensions()
    
    #   IMAGE MANAGER FUNCTIONS 
    def remove_background(self, image_path, image_title):
        self.image_manager.remove_image_background(image_path=image_path, image_title=image_title)

    def add_background(self, new_background):
        self.image_manager.add_new_background(new_background=new_background)


    
