# pytrunic
A python library for Trunic translation and script generation

## Overview

"Trunic" is the fictional writing system of the video game Tunic ([https://tunicgame.com/](https://tunicgame.com/)). Pytrunic is a light-weight, python-only library for rendering Trunic script from phonetic English strings.

For more on Trunic, see:
[https://www.thegamer.com/meaning-of-tunic-mysterious-language-andrew-shouldice/](https://www.thegamer.com/meaning-of-tunic-mysterious-language-andrew-shouldice/)
[https://www.reddit.com/r/TunicGame/comments/tgc056/tunic_language_reference_sheet_big_spoiler/](https://www.reddit.com/r/TunicGame/comments/tgc056/tunic_language_reference_sheet_big_spoiler/)

Trunic text is composed of "Trunes", each encoding a consonant/vowel pair of phonemes: multiple trunes are strung together to forms words. Example of Trunic text:

![Example Trunic](example_out001.png)

Phonetic translation: "t-roo-ni-k iz thzah l-ang-wi-ch ov thzah po-p-yoo-lah gay-m too-ni-k!"
English translation: "Trunic is the language of the popular game Tunic!"

## Usage
See "pytrunic_example.py":

    # create object to render Trunic
    trunic = Trunic(size=50, textcolour=(0,0,0))
    
    # Example sentence written in phoneme pairs
    sentence1 = 'doo yoo fear thzah iez ov thzah far shaw?'
    sentence2 = 't-roo-ni-k iz thzah l-ang-wi-ch ov thzah po-p-yoo-lah gay-m too-ni-k!'
    
    # Display in Trunic
    trunic.display(sentence1)
    
    # export out to file
    trunic.export(sentence2, 'example_out001.png')

## Notes of text strings and phonemes
I ended up using my own style of phonemes (see examples below). Each trune is specified by a combination of (up to two) phonemes (one consontant, one vowel in pronounced order), with individual trunes separated by a hyphen within a given word. Spaces between words. Accepts the punctuation . , ! and ?.

## Consonant phonemes:


## Vowel phonemes:
* 'a' as in **a**pple.
* 'ar'as in **ar**t.
* 'o' as in h**o**t.
* 'ay' as in d**ay**.
* 'e' as in 
* 'ee' as in 
* 'ear' as in 
* 'ah' as in 
* 'air' as in 
* 'i' as in 
* 'ie' as in 
* 'er' as in 
* 'oh' as in 
* 'oi' as in 
* 'oo' as in 
* 'ou' as in 
* 'ow' as in 
* 'aw' as in 

