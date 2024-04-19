from fractions import Fraction

pitch = ["c''", "d''", "e''", "g'", "a'"]
rhythm_list = ["4", "8", "16", "32", '8.', "16.", "8.."]

durations_fraction = {
    "1": Fraction(1),
    "r1": Fraction(1),
    "2": Fraction(1, 2),
    "r2": Fraction(1, 2),
    "4": Fraction(1, 4),
    "r4": Fraction(1, 4),
    "8": Fraction(1, 8),
    "r8": Fraction(1, 8),
    "16": Fraction(1, 16),
    "r16": Fraction(1, 16),
    "32": Fraction(1, 32),
    "r32": Fraction(1, 32),
    '2.': Fraction(3, 4),
    'r2.': Fraction(3, 4),
    '4.': Fraction(3, 8),
    'r4.': Fraction(3, 8),
    '8.': Fraction(3, 16),
    'r8.': Fraction(3, 16),
    '16.': Fraction(3, 32),
    'r16.': Fraction(3, 32),
    '32.': Fraction(3, 64),
    'r32.': Fraction(3, 64),
    '2..': Fraction(7, 8),
    'r2..': Fraction(7, 8),
    '4..': Fraction(7, 16),
    'r4..': Fraction(7, 16),
    '8..': Fraction(7, 32),
    'r8..': Fraction(7, 32),
    '16..': Fraction(7, 64),
    'r16..': Fraction(7, 64),
    '32..': Fraction(7, 128),
    'r32..': Fraction(7, 128)
}

frac_dotted_rest = [
    Fraction(3, 4),
    Fraction(3, 8),
    Fraction(3, 16),
    Fraction(3, 32),
    Fraction(3, 64),
    Fraction(7, 8),
    Fraction(7, 16),
    Fraction(7, 32),
    Fraction(7, 64),
    Fraction(7, 128)
]
dotted_rhythm_value_check = {
    Fraction(3, 4): (1, 2),
    Fraction(3, 8): (2, 4),
    Fraction(3, 16): (4, 8),
    Fraction(3, 32): (8, 16),
    Fraction(3, 64): (16,32)
}
dot_fraction_to_lilypond = {
    "3/4": "r2.",
    "3/8": "r4.",
    "3/16": "r8.",
    "3/32": "r16.",
    "3/64": "r32.",
    "7/8": "r2..",
    "7/16": "r4..",
    "7/32": "r8..",
    "7/64": "r16..",
    "7/128": "r32.."
}

note_fraction_to_lilypond = {
    3/4: "2.",
    "3/8": "4.",
    "3/16": "8.",
    "3/32": "16.",
    "3/64": "32.",
    "7/8": "2..",
    "7/16": "4..",
    "7/32": "8..",
    "7/64": "16..",
    "7/128": "32.."
}
fraction_to_lilypond = {
    Fraction(1, 1): "1",
    Fraction(1, 2): "2",
    Fraction(1, 4): "4",
    Fraction(1, 8): "8",
    Fraction(1, 16): "16",
    Fraction(1, 32): "32",
    Fraction(1, 64): "64",
    Fraction(1, 128): "128",
    Fraction(3, 2): "1.",
    Fraction(3, 4): "2.",
    Fraction(3, 8): "4.",
    Fraction(3, 16): "8.",
    Fraction(3, 32): "16.",
    Fraction(3, 64): "32.",
    Fraction(3, 128): "64.",
    Fraction(7, 4): "1..",
    Fraction(7, 8): "2..",
    Fraction(7, 16): "4..",
    Fraction(7, 32): "8..",
    Fraction(7, 64): "16..",
    Fraction(7, 128): "32.."
}
dotted_rest = [
    '2.', '4.', '8.', '16.', '32.', '2..', '4..', '8..', '16..', '32..'
]
