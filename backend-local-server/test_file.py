import os
from media_managment import MediaManager
from graphics_engine import GraphicsEngine

def test_loomis_generator():
    working_dir = r"C:\\Users\\sizib\\vs-code projects\\animation_studio-1"
    working_dir_home = os.path.join(working_dir, "backend-local-server")

    graphic = GraphicsEngine(working_dir=working_dir_home)

    graphic.run_female_loomis()

def test_grapics_engine():
    working_dir = r"C:\\Users\\sizib\\vs-code projects\\animation_studio-1"
    working_dir_home = os.path.join(working_dir, "backend-local-server")
    frames = os.path.join(working_dir, "backend-local-server","generation_output", "frames")
    video_output = os.path.join(working_dir, "backend-local-server", "generation_output", "video")
    image_output = os.path.join(working_dir, "backend-local-server", "generation_output", "images")
    audio_output = os.path.join(working_dir, "backend-local-server", "generation_output")
    
    print("Testing Graphics Engine")
    engine = GraphicsEngine(working_dir_home)

    engine.run_alegbra(chin_start=40, chin_end=60)
    #engine.run_edge_detection("2.png")

    #engine.run_plotting_sequence("2.png")

def main():
    working_dir = r"C:\\Users\\sizib\\vs-code projects\\animation_studio-1"
    working_dir_home = os.path.join(working_dir, "backend-local-server")
    frames = os.path.join(working_dir, "backend-local-server","generation_output", "frames")
    video_output = os.path.join(working_dir, "backend-local-server", "generation_output", "video")
    image_output = os.path.join(working_dir, "backend-local-server", "generation_output", "images")
    audio_output = os.path.join(working_dir, "backend-local-server", "generation_output")
    

    print("Testing audio extraction and additon ")
    print("Initialize audio manager")

    manager = MediaManager(working_dir=working_dir_home)
    #manager.init_sound_manager()

    #print("extracting audio")
    #manager.extract_sound("video_sample.mp4", "extracted.mp3")

    #print("Adding sound to video")
    #manager.add_sound("no_sound.mp4", "sample.mp3", "result.mp4")

    #print("Completed")
    
    

    print("Init...")
    manager.init_video_manager(title="Test-004.mp4", frames=frames, output=video_output)
    manager.init_image_manager(image_output, frames)

    print("Breaking video into frames ")
    #manager.break_into_frames("no_sound.mp4")

    test_image = os.path.join(working_dir_home, "2.png")
    print("Remove background")
    manager.remove_background(test_image, "test.png")

    #   TESTING PLOT 
    

    ''''
    test_background = "background.png"

    print("Removing background singular image")
    manager.init_image_manager(image_output, frames)
    #manager.remove_background("2.png", "Test-002.png")

    print("Removing background - batch images")
    manager.add_background(test_background)

    print("Updating source path ")
    manager.update_source(image_output)
    
    print("Render into video")
    print("Running equalizer")
    manager.equalize_dimensions()
    print("Rendering")
    manager.render_frames_to_video()
    print("Running garbage collection")
    manager.garbage_collection()
    '''




if __name__ == "__main__":
    test_grapics_engine()
