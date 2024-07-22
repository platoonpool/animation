import math
import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw
bone_image = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
draw = ImageDraw.Draw(bone_image)
draw.rectangle((20, 30, 80, 70), fill='gray')
draw.ellipse((10, 20, 30, 40), fill='gray')
draw.ellipse((10, 60, 30, 80), fill='gray')
draw.ellipse((70, 20, 90, 40), fill='gray')
draw.ellipse((70, 60, 90, 80), fill='gray')
bone_image.save('bone.png')
dog_image = Image.new('RGB', (100, 100), color='white')
draw = ImageDraw.Draw(dog_image)
draw.ellipse((20, 20, 80, 80), fill='brown')  # Head
draw.rectangle((45, 50, 55, 90), fill='brown')  # Body
dog_image.save('image2.png')
video_clip = VideoFileClip("video.mp4")
cat_clip = ImageClip("image.png").set_duration(video_clip.duration)
dog_clip = ImageClip("image2.png").set_duration(video_clip.duration)
bone_clip = ImageClip("bone.png").set_duration(video_clip.duration)
center_x = video_clip.size[0] / 2 - cat_clip.size[0] / 2
center_y = video_clip.size[1] / 2 - cat_clip.size[1] / 2
radius = 100


def circular_motion(t):
    return center_x + radius * np.cos((t / video_clip.duration) * 4 * math.pi), center_y + radius * np.sin((t / video_clip.duration) * 2 * math.pi)


cat_clip = cat_clip.set_position(circular_motion)
bone_position_top_right = (video_clip.size[0] - bone_clip.size[0], 0)
dog_position = (video_clip.size[0] - dog_clip.size[0], video_clip.size[1] - dog_clip.size[1])
bone_clip_top_right = bone_clip.set_position(bone_position_top_right)
dog_clip = dog_clip.set_position(dog_position)
final_clip = CompositeVideoClip([video_clip, cat_clip, bone_clip_top_right, dog_clip])
audio_clip = AudioFileClip("audio.mp3")
audio_clip = audio_clip.subclip(0, video_clip.duration)
final_clip = final_clip.set_audio(audio_clip)
final_clip.write_videofile("output_with_audio.mp4", fps=video_clip.fps)
video_clip.close()
