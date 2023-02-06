# pytrunic: python library for Trunic translation and script generation
#
# by mit-mit
#

import os
from PIL import Image, ImageDraw, ImageFont

# dictionary for symbols
vowels = {}
vowels['a'] = [0,1,2]
vowels['ar'] = [0,1,3,4]
vowels['o'] = [1,2]
vowels['ay'] = [1]
vowels['e'] = [2,3,4]
vowels['ee'] = [1,2,3,4]
vowels['ear'] = [1,2,4]
vowels['ah'] = [0,1]
vowels['air'] = [2,4]

vowels['i'] = [3,4]
vowels['ie'] = [0]
vowels['er'] = [0,2,3,4]
vowels['oh'] = [0,1,2,3,4]
vowels['oi'] = [3]
vowels['oo'] = [0,1,2,3]
vowels['ou'] = [2,3]
vowels['ow'] = [4]
vowels['aw'] = [0,1,2,4]

cons = {}
cons['b'] = [1,3]
cons['ch'] = [2,4]
cons['d'] = [1,3,5]
cons['f'] = [0,4,5]
cons['g'] = [0,3,4]
cons['h'] = [1,3,4]
cons['j'] = [1,5]
cons['k'] = [0,1,3]
cons['l'] = [1,4]

cons['m'] = [3,5]
cons['n'] = [2,3,5]
cons['ng'] = [0,1,2,3,4,5]
cons['p'] = [0,4]
cons['r'] = [0,1,4]
cons['s'] = [0,1,4,5]
cons['sh'] = [0,2,3,4,5]
cons['t'] = [0,2,4]
cons['th'] = [0,1,2,4]

cons['thz'] = [1,3,4,5]
cons['v'] = [1,2,3]
cons['w'] = [0,2]
cons['y'] = [1,2,4]
cons['z'] = [1,2,3,4]
cons['zh'] = [0,1,2,3,5]

class Trunic:
    def __init__(self, size=50, textcolour='black', bgcolor='white', 
        max_width=800, linespace=0.5, wordspace=0.5):
        self.vcoords = [(0.5,-1.0,1.0,-0.66), 
            (0.0,-0.66,0.5,-1.0), 
            ( (0.0,0.0,0.0,-0.66), (0.0,0.66,0.0,0.33) ),
            (0.0,0.66,0.5,1.0),
            (0.5,1.0,1.0,0.66)]
        self.ccoords = [( (0.5,-0.33,1.0,-0.66), (0.5,0.0,0.5,-0.33) ),
            ( (0.5,-0.33,0.5,-1.0), (0.5,0.0,0.5,-0.33) ),
            ( (0.5,-0.33,0.0,-0.66), (0.5,0.0,0.5,-0.33) ),
            (0.5,0.33,1.0,0.66),
            (0.5,0.33,0.5,1.0),
            (0.5,0.33,0.0,0.66)]
            
        self.size = size
        self.linespace = linespace
        self.wordspace = wordspace
        self.textcolour = textcolour
        self.bgcolor = bgcolor
        self.linewidth = int(self.size/10)
        
        self.w = max_width
        self.h = int(self.size*(2 + 2*self.linespace))
        
        self.reset_image()
        
        self.punc_start_space = 0.2
        self.punc_end_space = 0.5
    
    def reset_image(self, sentence=None):
        self.offset = [self.size*self.wordspace, self.size*(1.0+self.linespace)]
        if not sentence is None:
            self.h = self.check_h_needed(sentence)
        self.img = Image.new("RGB", (self.w, self.h), color=self.bgcolor)
        self.imgdr = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype(os.path.join('font','ArialNarrow7-9YJ9n.ttf'),self.size)
    
    def isvowel(self, l):
        if l in ['a','e','i','o','u']:
            return True
        else:
            return False
    
    def get_cind(self, str):
        for (i,l) in enumerate(str):
            if not self.isvowel(l):
                return i
        return None
    
    def get_vind(self, str):
        for (i,l) in enumerate(str):
            if self.isvowel(l):
                return i
        return None
    
    def check_v(self, v):
        if v in vowels.keys():
            return v
        else:
            print('Unknown vowel phoneme: %s'%(v))
            return None
    
    def check_c(self, c):
        if c in cons.keys():
            return c
        else:
            print('Unknown const phoneme: %s'%(c))
            return None
    
    # get_vc_pair: splits single phoneme into vowel/const parts, and determines order
    def get_vc_pair(self, phone):
        if self.isvowel(phone[0]):
            cind = self.get_cind(phone)
            if cind is None:
                c = None
                v = self.check_v(phone)
                circle = 0
            else:
                # determine if cons is part of vowel
                if phone[0:(cind+1)] in vowels.keys():
                    v = self.check_v(phone[0:(cind+1)])
                    if len(phone) > (cind+1):
                        c = self.check_c(phone[(cind+1):])
                        circle = 1
                    else:
                        c = None
                        circle = 0
                else:
                    v = self.check_v(phone[0:cind])
                    c = self.check_c(phone[cind:])
                    circle = 1
        else:
            vind = self.get_vind(phone)
            if vind is None:
                c = self.check_c(phone)
                v = None
            else:
                v = self.check_v(phone[vind:])
                c = self.check_c(phone[0:vind])
            circle = 0
        
        return (v, c, circle)
    
    def draw_trune(self, c=None, v=None, circle=0):
        
        # determine edges list for trune
        if v is None:
            vlist = []
        else:
            vlist = vowels[v]
        
        if c is None:
            clist = []
        else:
            clist = cons[c]
        
        # Render anchor line
        x1 = self.offset[0]
        y1 = self.offset[1]
        x2 = self.size + self.offset[0]
        y2 = self.offset[1]
        self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
        
        # Render trune edges at current cursor
        for vi in vlist:
            if type(self.vcoords[vi][0]) is tuple:
                x1 = self.size*self.vcoords[vi][0][0] + self.offset[0]
                y1 = self.size*self.vcoords[vi][0][1] + self.offset[1]
                x2 = self.size*self.vcoords[vi][0][2] + self.offset[0]
                y2 = self.size*self.vcoords[vi][0][3] + self.offset[1]
                self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
                x1 = self.size*self.vcoords[vi][1][0] + self.offset[0]
                y1 = self.size*self.vcoords[vi][1][1] + self.offset[1]
                x2 = self.size*self.vcoords[vi][1][2] + self.offset[0]
                y2 = self.size*self.vcoords[vi][1][3] + self.offset[1]
                self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
            else:
                x1 = self.size*self.vcoords[vi][0] + self.offset[0]
                y1 = self.size*self.vcoords[vi][1] + self.offset[1]
                x2 = self.size*self.vcoords[vi][2] + self.offset[0]
                y2 = self.size*self.vcoords[vi][3] + self.offset[1]
                self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
        for ci in clist:
            if type(self.ccoords[ci][0]) is tuple:
                x1 = self.size*self.ccoords[ci][0][0] + self.offset[0]
                y1 = self.size*self.ccoords[ci][0][1] + self.offset[1]
                x2 = self.size*self.ccoords[ci][0][2] + self.offset[0]
                y2 = self.size*self.ccoords[ci][0][3] + self.offset[1]
                self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
                if c in ['w','n']:
                    continue # no vertical line in these trunes, so no connection drawn
                x1 = self.size*self.ccoords[ci][1][0] + self.offset[0]
                y1 = self.size*self.ccoords[ci][1][1] + self.offset[1]
                x2 = self.size*self.ccoords[ci][1][2] + self.offset[0]
                y2 = self.size*self.ccoords[ci][1][3] + self.offset[1]
                self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
            else:
                x1 = self.size*self.ccoords[ci][0] + self.offset[0]
                y1 = self.size*self.ccoords[ci][1] + self.offset[1]
                x2 = self.size*self.ccoords[ci][2] + self.offset[0]
                y2 = self.size*self.ccoords[ci][3] + self.offset[1]
                self.imgdr.line([(int(x1),int(y1)),(int(x2),int(y2))], fill=self.textcolour, width=self.linewidth)
        
        # Render circle
        if circle == 1:
            x1 = self.size*0.35 + self.offset[0]
            y1 = self.size + self.offset[1]
            x2 = self.size*0.65 + self.offset[0]
            y2 = self.size + 0.3*self.size + self.offset[1]
            self.imgdr.ellipse((int(x1), int(y1), int(x2), int(y2)), outline=self.textcolour, width=self.linewidth)
    
    def next_letter(self):
        self.offset[0] += self.size
    
    def next_word(self):
        self.offset[0] += self.size*self.wordspace
    
    def start_punc(self):
        self.offset[0] += self.size*self.punc_start_space
    
    def end_punc(self):
        self.offset[0] += self.size*self.punc_end_space
    
    def check_lineend(self, nextlen, offset):
        if (offset[0] + nextlen*self.size + self.size*self.wordspace) > self.w:
            offset[0] = self.size*self.wordspace
            offset[1] += 2*self.size + self.size*self.linespace
        return offset
    
    def check_h_needed(self, sentence):
        words = sentence.split()
        offset_temp = [self.offset[0], self.offset[1]]
        for word in words:
            phones = word.split('-')
            offset_temp = self.check_lineend(len(phones), offset_temp)
            for (i,phone) in enumerate(phones):
                if phone[-1] in ['.',',','?','!']:
                    punc = phone[-1]
                    phone = phone[:-1]
                else:
                    punc = None
                (v, c, circle) = self.get_vc_pair(phone)
                offset_temp[0] += self.size
                if not punc is None:
                    offset_temp[0] += self.size*self.punc_start_space
                    offset_temp[0] += self.size*self.punc_end_space
                    
            offset_temp[0] += self.size*self.wordspace
        
        return int(offset_temp[1]+self.size+self.size*self.linespace)
    
    def render_phonemes(self, sentence):
        words = sentence.split()
        check = []
        for word in words:
            phones = word.split('-')
            self.check_lineend(len(phones), self.offset)
            for (i,phone) in enumerate(phones):
                if phone[-1] in ['.',',','?','!']:
                    punc = phone[-1]
                    phone = phone[:-1]
                else:
                    punc = None
                (v, c, circle) = self.get_vc_pair(phone)
                check.append((v, c, circle))
                self.draw_trune(c=c, v=v, circle=circle)
                self.next_letter()
                if not punc is None:
                    self.start_punc()
                    box = self.font.getbbox(punc)
                    x = self.offset[0]
                    y = self.offset[1]-0.9*box[3]
                    if punc in ['?','!']:
                        y += 0.4*box[3]
                        
                    self.imgdr.text((x, y), punc, fill=self.textcolour, font=self.font)
                    self.end_punc()
                    
            self.next_word()
            check.append('-')
    
    def display(self, sentence):
        self.reset_image(sentence)
        self.render_phonemes(sentence)
        self.img.show()
    
    def export(self, sentence, output_path):
        self.reset_image(sentence)
        self.render_phonemes(sentence)
        self.img.save(output_path)

