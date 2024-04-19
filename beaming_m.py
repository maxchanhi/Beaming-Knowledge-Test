import random
from fractions import Fraction
import copy

from notation import *


#Generate wrong options
def insert_brackets_randomly(melody, num_pairs):
  melody_list=[]
  for note in melody:
    melody_list.append(note[0])
  for _ in range(num_pairs):
    # Ensure there is at least one note between brackets
    left_bracket_pos = random.randint(0, len(melody_list) - 2)  # -2 to
    right_bracket_pos = random.randint(
        left_bracket_pos + 1,
        len(melody_list) -
        1)  # Ensure right bracket comes after the left bracket

    melody_list.insert(left_bracket_pos, "[")  # Insert left bracket
    melody_list.insert(
        right_bracket_pos + 1,
        "]")  # Insert right bracket, +1 due to the left bracket insertion
  return melody_list


#check if the wrong option is correct, regenerate
def check_brackets_at_beats(melody, lowertime):
  rhythm_in_melody =[]
  beat_cutter = []
  beat_jot = [0]
  for note in melody:
    rhythm_in_melody.append(note[1])
  for i in range(len(rhythm_in_melody)):
    beat_cutter.append(rhythm_in_melody[i])
    duration_sum = sum(beat_cutter)
    if duration_sum % (1 / lowertime) == 0:
      beat_jot.append(i + 1)  # +1 because i starts from 0
      beat_cutter.clear()  # Using clear as a method

  beat_jot.append(len(rhythm_in_melody) + 1)
  melody_with_brackets =[]
  for note in melody:
    melody_with_brackets.append(note[0])
  # Find bracket positions
  opening_brackets = [
      i for i, x in enumerate(melody_with_brackets) if x == "["
  ]
  closing_brackets = [
      i for i, x in enumerate(melody_with_brackets) if x == "]"
  ]

  for bracket_pos in opening_brackets + closing_brackets:
    if bracket_pos in beat_jot:
      return False
  return True

def main_wrong(melody,lowertime):
  plain_melody =[]
  for note in plain_melody:
    plain_melody.append(note[0])
  blacket_melody = insert_brackets_randomly(melody,1)
  if  check_brackets_at_beats(melody,lowertime) == False:
    print("regenerate main wrong")
    return main_wrong(melody=melody,lowertime=lowertime)
  else:
    return blacket_melody


# For correct answer
def correct_answer(melody, uppertime,lowertime):
  melody=main_grouping(melody,uppertime,lowertime)
  melody=main_restgrouping(melody)
  melody = swap_rest(melody)
  return melody

def swap_rest(melody):
  rest_list = []
  for note in melody:
    if "r" in note[0]:
      rest_list.append(note[1])

  if len(rest_list) > 0:
    rest_list = remove_duplicates(rest_list)
    rest_list.sort(reverse=True)
    print("rest_list", rest_list)
    change_mem =[]
    for rest_check in rest_list:
      main_beat = []
      p = value = 0
      for note in melody:
        value+= note[1]
        if value % rest_check ==0:
          main_beat.append(p)
        p+=1
      print(main_beat)
      for pos in main_beat:
        if "r" in melody[pos][0] and "r" in melody[pos-1][0] and pos not in change_mem:
          if melody[pos][1]+melody[pos-1][1]>=rest_check:
            last_rest = change_arest(rest_check)
            front_rest = melody[pos][1]+melody[pos-1][1]-rest_check
            melody[pos] = last_rest
            change_mem.append(pos)
            if front_rest:
              melody[pos-1] = change_arest(front_rest)
  
  return melody


def change_note_based_on_fraction(note, tie=False):
  lily, fraction = note
  if '.' in lily:
    lily = lily.replace('.', '')
    rhythm_value = int(fraction.denominator)

    pitch, octave = lily.split("'")
    if tie == False:
      lily = pitch + "'" + str(rhythm_value)
    elif tie == True:
      lily = pitch + "'" + str(rhythm_value) + "~"
  else:
    pass
  return [lily, fraction]


# fix note group but not rest
def seperate_note(note_to_change, stnew_note, nd_note):
  pitch, _ = note_to_change
  st_new_rhythm = fraction_to_lilypond[stnew_note]
  nd_new_rhythm = fraction_to_lilypond[nd_note]
  pitch = pitch.split("'")[0]
  return [[pitch + "'" + st_new_rhythm + "~", stnew_note],
          [pitch + "'" + nd_new_rhythm, nd_note]]
def change_note(note_to_change, new_duration):
  pitch, octave = note_to_change[0].split("'")
  rhythm_value = int( Fraction(1,new_duration))
  return [pitch+"'"+str(rhythm_value),new_duration]


def beat_cutter(melody, check, session=0):
  main_beat = []
  value = beat_p = 0
  for note in melody:
    value += note[1]
    if value == Fraction(1, check) or note[1]>=Fraction(1, check):
      value = 0
    if value > Fraction(1, check):
      main_beat.append([beat_p, value])
      value = 0
    beat_p += 1

  if main_beat:
    beat_pos,beat_value = main_beat[0]
    ex_beat = beat_value - Fraction(1, check)
    in_beat = melody[beat_pos][1] - ex_beat
    if ex_beat and in_beat:
      melody[beat_pos:beat_pos + 1] = seperate_note(melody[beat_pos], in_beat,ex_beat)
      return beat_cutter(melody, check, session=0)
  """if session < len(melody) // 4:
    return beat_cutter(melody, check, session + 1)"""
  return melody


def main_grouping(melody,uppertime, lowertime):
  if uppertime == 3 or uppertime == 9:
    rhythm_checklist = [lowertime]
  else:
    rhythm_checklist = [lowertime // 2, lowertime]
  for check_value in rhythm_checklist:
    melody = beat_cutter(melody, check_value)
  return melody

import re
#fix rest
def extract_duration_digit(note_string):

    match = re.search(r'\d+', note_string)
    if match:
        return int(match.group())
    else:
        raise ValueError("No duration digit found in the string.")
def change_rests( stnote, nd_note):
  st_new_rhythm = fraction_to_lilypond[stnote]
  nd_new_rhythm = fraction_to_lilypond[nd_note]
  rest = "r"
  return [[rest + st_new_rhythm ,stnote],
          [rest + nd_new_rhythm,nd_note]]

def change_arest(frac):
  st_new_rhythm = fraction_to_lilypond[frac]
  return ["r"+ st_new_rhythm ,frac]


def rest_beat_cutter(melody, check):
  main_beat = []
  value = beat_p = 0
  check_value= check[0]
  for note in melody:
    value += note[1]
    if value >= Fraction(1, check_value) :
      if "r" in note[0]:
        main_beat.append([beat_p, value])
      value = 0
    beat_p += 1
  for beat in main_beat:
    if  melody[beat[0]][1] >= Fraction(1, check_value):
      ex_beat = beat[1] - Fraction(1, check_value)
      in_beat = melody[beat[0]][1] - ex_beat
      if ex_beat and in_beat:
        melody[beat[0]:beat[0] + 1] = change_rest(in_beat, ex_beat)
    return melody

def main_restgrouping(melody):
  rhythm_checklist = []
  position = 0
  for note in melody:
    if "r" in note[0]:
      c_value = extract_duration_digit(note[0])
      rhythm_checklist.append([c_value,position])
    position+= 1
  for check_value in rhythm_checklist:
    melody = rest_beat_cutter(melody, check_value)
  return melody


