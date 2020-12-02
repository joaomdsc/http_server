# fake_text.py - Joao's python plugin for Nagios

import sys
from random import randrange

from faker import Faker
fake = Faker()

def paragraph(n):
    """Generate a paragraph of n lines with 7 words each."""
    lines = []
    for i in range(n):
        lines.append(fake.sentence(nb_words=7))
    return '\n'.join(lines)

state = randrange(0, 4)
out = (0, 'OK', "Everything's just fine") if state == 0 \
  else (1, 'Warning', 'Careful, not looking good') if state == 1 \
  else (2, 'Critical', "Oops, now we're in trouble") if state == 2 \
  else (3, 'Unknown', "I have no idea what's going on")

first_line = f'{out[1]}: {out[2]}'

first_perfdata = fake.sentence(nb_words=7)

other_output = paragraph(4)
other_perfdata = paragraph(4)

print(f'{first_line} | {first_perfdata}')
print(f'{other_output} | {other_perfdata}')

sys.exit(out[0])