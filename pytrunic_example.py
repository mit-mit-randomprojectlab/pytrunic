# pytrunic_example.py: Example use of pytrunic for rendering out Trunic
# from English phonemes

from pytrunic import Trunic

# create object to render Trunic
trunic = Trunic(size=50, textcolour=(0,0,0))

# Example sentence written in phoneme pairs
sentence1 = 'doo yoo fear thzah iez ov thzah far shaw?'
sentence2 = 't-roo-ni-k iz thzah l-ang-wi-ch ov thzah po-p-yoo-lah gay-m too-ni-k!'

# Display in Trunic
trunic.display(sentence1)

# export out to file
trunic.export(sentence2, 'example_out001.png')
