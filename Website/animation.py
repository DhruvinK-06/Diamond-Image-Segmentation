import os
# importing editor from movie py
from moviepy.editor import *
# Get the list of all files and directories
# in the root directory
path = "D:/Development- Project/reddit-video-downloader-python-main/Shape_1d_256i/AS"
dir_list = os.listdir(path)
  
print("Files and directories in '", path, "' :") 
  
# print the list
print(dir_list)



  
# creating a Image sequence clip with fps = 1
clip = ImageSequenceClip(['frame1.png', 'frame2.png', 'frame1.png', 'frame2.png'], fps = 1)
  
# showing  clip 
clip.ipython_display(width = 360) 