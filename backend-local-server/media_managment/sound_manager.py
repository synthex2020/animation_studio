from moviepy import VideoFileClip, AudioFileClip
import os 



class SoundManager:

    def __init__(self, output ):
        self.output_folder = output

    
    #   EXTRACT SOUND FROM VIDEO 
    def extract_sound(self, video_file, title):
        #   LOAD THE VIDEO CLIP 
        video_clip = VideoFileClip(video_file)

        #   EXTRACT THE AUDIO 
        audio_clip = video_clip.audio

        #   OUTPUT FOLDER 
        audio_file_output = os.path.join(self.output_folder, "audio")

        #   WRITE AUDIO TO FILE 
        audio_clip.write_audiofile(audio_file_output)

        #   CLOSE THE VIDEO AND AUDIO CLIPS
        audio_clip.close()
        video_clip.close()

    #   ADD SOUND TO VIDEO 
    def add_sound(self, video_file, audio_file, title):
        #   LOAD THE RESPECTIVE CLIPS 
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)

        #   OUTPUT FOLDER 
        output_video_folder = os.path.join(self.output_folder, "video")
        output_video_title = os.path.join(output_video_folder, title)

        #   ENSURE THEY ARE THE SAME LENGTH IF NOT VIDEO CLIP LENGTH MATCHES AUDIO CLIP 
        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclipped(0, video_clip.duration)

        #   ADDING AUDIO TO THE CLIP 
        resultant_video = video_clip.with_audio(audio_clip)
        
        #   WRITING TO FILE 
        resultant_video.write_videofile(output_video_title, codec="libx264", audio_codec="aac")

        #   DESTROY THE OBJECTS 
        video_clip.close()
        audio_clip.close()
        
    

    


