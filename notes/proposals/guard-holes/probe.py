import sys; sys.path.insert(0,'source'); import propose as p
change=['Shall I change the render tool so it reuses cached frames? Y/N',
 'Y or N: add a new gate before every clip?',
 'Y or N: add a new gate to pre-flight?',
 'Need: Y or N to make finish.py add the sign-off twice?',
 '1. Y or N: should every animatic now get a second critic pass? (my pick Y)',
 'Shall I make the subtitles bigger in every film from now on? Y/N',
 'Y or N: from now on, voices are recorded at 48 kHz?',
 'Y or N: switch every film to 30 fps?',
 'OK to update the house look so mouths draw at rest? Y/N',
 '2. Y or N: write the lesson into the rulebook? (my pick Y)',
 'Shall I add a check sheet step before every clip? Y/N',
 'Y or N: change how the sheet is laid out for every round?']
routine=['Need: Y or N for the animatic',
 'Final render next, about 9 min. Go ahead? Y/N',
 '1. Y or N: send the clip of seconds 4-7? (my pick Y)',
 'Shall I post it to TikTok now? Y/N',
 'Y or N: restart Protest Tiers now? (my pick Y)',
 '1. Which hook text: 1 or 2? (my pick 1)',
 'Y or N: is the beaver too big in shot 3?',
 'Shall I fix note 8 by moving the whale left? Y/N',
 'Y or N: use photo 2 as the reference for the town hall?',
 'Need: Y or N to rerender shot 4 with the new hands?']
m=[q for q in change if not p.reply_faults(q)]; f=[q for q in routine if p.reply_faults(q)]
print(f'change asks missed: {len(m)}/{len(change)}'); [print('  MISS',q) for q in m]
print(f'routine asks blocked: {len(f)}/{len(routine)}'); [print('  BLOCK',q) for q in f]
