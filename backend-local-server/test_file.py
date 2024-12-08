import os
from media_managment import MediaManager

def main():
    working_dir = r"C:\\Users\\sizib\\vs-code projects\\animation_studio-1"
    frames = os.path.join(working_dir, "backend-local-server","generation_output", "frames")
    video_output = os.path.join(working_dir, "backend-local-server", "generation_output", "video")
    image_output = os.path.join(working_dir, "backend-local-server", "generation_output", "images")
    manager = MediaManager(working_dir=working_dir)

    print("Init...")
    manager.init_video_manager(title="Test-001.mp4", frames=frames, output=video_output)

    print("Breaking video into frames ")
    manager.break_into_frames("no_sound.mp4")

    '''
    print("Init complete, moving on to processing images")
    
    manager.equalize_dimensions()
    manager.render_frames_to_video()
    manager.garbage_collection()

    '''
    test_background = "background.png"

    print("Removing background singular image")
    manager.init_image_manager(image_output, frames)
#   manager.remove_background(test_image, "Test-002.png")

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

if __name__ == "__main__":
    main()


