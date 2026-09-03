from moviepy.editor import *
import os

def render_video(image_sequence, audio_file, output_path="output/final_video.mp4"):
    if not os.path.exists("output"):
        os.makedirs("output")
    
    audio = AudioFileClip(audio_file)
    total_duration = audio.duration
    clip_duration = total_duration / len(image_sequence)

    clips = []
    for i, img_name in enumerate(image_sequence):
        img_path = os.path.join("assets/images", img_name)
        # Ken Burns Effect
        if i % 2 == 0:
            clip = (ImageClip(img_path).resize(lambda t: 1 + 0.04 * (t / clip_duration)).set_duration(clip_duration))
        else:
            clip = (ImageClip(img_path).resize(lambda t: 1.04 - 0.04 * (t / clip_duration)).set_duration(clip_duration))
        
        # 1080p Crop
        clip = clip.resize(height=1080).crop(x_center=clip.w/2, y_center=clip.h/2, width=1920, height=1080)
        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_audio(audio)

    final_video.write_videofile(
        output_path, fps=30, codec='libx264', audio_codec='aac', bitrate='8000k', threads=4
    )
    print(f"🎬 Video saved at: {output_path}")
