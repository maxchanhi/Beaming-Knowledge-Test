import random
from fractions import Fraction

from notation import *


def rhythm_generation(all_rhythm_list, number_of_beat, lowertime):
  available_list = all_rhythm_list[:]
  beat_amount = Fraction(1, lowertime)
  melody = []
  melody_duration_sum = 0

  while melody_duration_sum < number_of_beat * beat_amount:
    rhythm_choice = random.choice(available_list)
    melody.append(rhythm_choice)
    melody_duration_sum += durations_fraction[rhythm_choice]

    if melody_duration_sum % beat_amount == 0:
      available_list = all_rhythm_list[:]
    else:
      # Update available_list based on remaining beat amount
      remaining_beat = beat_amount - (melody_duration_sum % beat_amount)
      available_list = [
          rhythm for rhythm in all_rhythm_list
          if durations_fraction[rhythm] <= remaining_beat
      ]

  return melody


def insert_note_rest(rhythm_in_melody,
                     uppertime,
                     pitch_a=4,
                     max_attempts=10,
                     current_attempt=0):
  lily_melody = []
  pitch_c = 0
  rest_c = 0
  simpletime = uppertime in [2, 3, 4]
  for rhythm in rhythm_in_melody:
    if random.randint(0, 1) == 0:
      if (simpletime is True
          and rhythm not in dotted_rest) or (simpletime is False):
        note_with_rhythm = f"r{rhythm}"
        lily_melody.append(note_with_rhythm)
        rest_c += 1
      else:
        note_pitch = random.choice(pitch)
        note_with_rhythm = f"{note_pitch}{rhythm}"
        lily_melody.append(note_with_rhythm)
        pitch_c += 1
    else:
      # If the random condition for rest was not met, just add a pitch note
      note_pitch = random.choice(pitch)
      note_with_rhythm = f"{note_pitch}{rhythm}"
      lily_melody.append(note_with_rhythm)
      pitch_c += 1

  if (pitch_c < pitch_a
      or rest_c < pitch_a / 2) and current_attempt < max_attempts:
    return insert_note_rest(rhythm_in_melody,
                            uppertime=uppertime,
                            pitch_a=pitch_a,
                            max_attempts=max_attempts,
                            current_attempt=current_attempt + 1)
  elif current_attempt >= max_attempts:
    lily_melody = []
    return False

  return lily_melody


def note_with_fraction(melody):
  result = []
  for note in melody:
    rhythm_value = ''.join(filter(str.isdigit, note))
    dots = note.count('.')
    if rhythm_value:  # Check if we have a numeric rhythm value
      rhythm_fraction = Fraction(1, int(rhythm_value))
      for _ in range(dots):
        rhythm_fraction += rhythm_fraction / 2
    else:
      raise ValueError(f"No rhythm value found in note '{note}'")
    result.append([note, rhythm_fraction])
  return result


def main_generation(rhythm_list, lowertime, uppertime):
  melody = rhythm_generation(rhythm_list, uppertime, lowertime)
  melody_rest = insert_note_rest(melody, uppertime)
  while melody_rest is False or len(melody_rest) < 8:
    melody_rest = rhythm_generation(rhythm_list, uppertime, lowertime)
    melody_rest = insert_note_rest(melody, uppertime)
  return note_with_fraction(melody_rest)


