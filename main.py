from fractions import Fraction
from notation import fraction_to_lilypond
from melody_gen import *
from beaming_m import *
import copy
import random
import subprocess
from PIL import Image
import os

def lilypond_generation(melody,name,uppertime,lowertime):
  lilypond_score = f"""
\\version "2.25.12"  
\\header {{
tagline = "" 
}}

#(set-global-staff-size 26)

\\score {{
\\fixed c'' {{
  \\time {uppertime}/{lowertime}
  {melody}
  \\bar "|"
}}
\\layout {{
  indent = 0\\mm

  ragged-right = ##f
  \\context {{
    \\Score

    \\remove "Bar_number_engraver"
  }}
}}
}}
"""

  with open('score.ly', 'w') as f:
    f.write(lilypond_score)

    subprocess.run(['lilypond', '--png', '-dresolution=300', 'score.ly'], check=False)

  with Image.open('score.png') as img:
    width, height = img.size
    crop_height = height
    crop_rectangle = (0, 75, width, crop_height/10)

    cropped_img = img.crop(crop_rectangle)
    cropped_img.save(f'cropped_score_{name}.png')


uppertime=lowertime = 4
rhythm_list = ["4", "8", "16", "32", '8.', "16."]

melody=main_generation(rhythm_list,uppertime,lowertime)

print("Raw melody",melody)
correct_melody = copy.deepcopy(melody)
correct_melody= correct_answer(correct_melody,uppertime,lowertime)
print("Correct melody",correct_melody)

wrong_melody_list = []
i=0
while len(wrong_melody_list)<5:
  wrong_melody_list.append([i,main_wrong(melody,lowertime)])
  i+= 1
  wrong_melody_list.append([i,main_wrong(correct_melody,lowertime)])
  i+= 1

for melody in wrong_melody_list:
  lilypond_generation(melody[1],melody[0],uppertime,lowertime)
