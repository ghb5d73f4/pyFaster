#!/usr/env python
'''
 -*- coding: utf-8 -*-
 -*- format: python -*-
 -*- author: G. Henning -*-
 -*- created: 2018-06-18 -*-
 -*- copyright: GH/IPHC 2018 -*-
 -*- file: read_faster.py -*-
 -*- purpose: Read FASTER events -*-
'''


import struct
import os
from cStringIO import StringIO as StringBuffer

class FasterData(object):
    def __init__(self, header,
                 data):
        self.type_alias=header['type_alias']
        self.magic=header['magic']
        self.time = header['clock1']+header['clock2']*255.+\
            header['clock3']*255*255+header['clock4']*255*255*255+\
            header['clock5']*255*255*255*255+header['clock6']*255*255*255*255*255
        self.label=header['label']
        self.load_size=header['load_size']/256
        self.data=data
        if self.type_alias==70:
            self._unpack_type_70()
        elif self.type_alias==10:
            self._unpack_type_10()
        elif self.type_alias==61:
            self._unpack_type_61()
        pass

    def _unpack_type_61(self):
        the_data = self.data
        high, low = struct.unpack("!LL", the_data)
        delta_t = high & 0x003FFFC0  >>6
        measure = low & 0xFFFFFC00 >> 10
        rnge= low & 0x00000380 >> 7
        saturated=low & 0x00000002 >> 1
        pileup= low & 0x00000001 >> 7
        self.data = {'dt':delta_t,
                     'value':measure,
                     'range':rnge,
                     'saturated':int(saturated),
                     'pileup':int(pileup)}

    def _unpack_type_10(self):
        '''unpack Group data'''
        # A group is just some generic events...
        the_data=StringBuffer(self.data)
        group_evt = []
        head_data =the_data.read(struct.calcsize(FasterFileReader._header_fmt))
        while(head_data):
            header = FasterFileReader.read_header(head_data)
            evt_data = FasterFileReader.read_data(the_data, header)
            group_evt.append(FasterData(header, data=evt_data))
            head_data =the_data.read(struct.calcsize(FasterFileReader._header_fmt))
            pass
        self.data = group_evt
        
        

    def _unpack_type_70(self):
        '''unpack ADC scaler data'''
        the_data=self.data
        if not len(the_data)==struct.calcsize('!LLL'):
            return 0
        calc,sent,trig = struct.unpack("!LLL", the_data)
        self.data = {'calc':calc, 'sent':sent, 'trig':trig}

    def _repr_head(self):
        return "<FasterData TYPE={s.type_alias}, CLOCK={s.time}, LABEL={s.label}, MAGIC={s.magic}, LOAD_SIZE={s.load_size}>".format(s=self)

    def __repr__(self):
        return "<FasterData TYPE={s.type_alias}, CLOCK={s.time}, LABEL={s.label}, MAGIC={s.magic}, LOAD_SIZE={s.load_size}, DATA='{s.data}'>".format(s=self)
    pass


class FasterFileReader(object):
    """Stream FASTER events from file"""

    _header_fmt = "! B B BBBBBB H H"
#    _header_size = struct.calcsize(FasterFileReader._header_fmt) 


    def __init__(self, evtfile="", maxnevents=-1):
        """Creator
        
        Keyword arguments:
        evtfile -- path to file to stream
        maxnevents -- number of events to read at most (default = -1 i.e. infinity
        """
        self.fpath = evtfile
        self.infile = None
        self.fmt = self._header_fmt
        self._header_size = struct.calcsize(self._header_fmt)
        self.maxnevents=maxnevents
        self._nevent=0
        if (evtfile!=""):
            self.open(self.fpath)
            pass
        pass

    def __repr__(self):
        return "<FasterFileReader '{s.fpath}'>".format(s=self)
    
    def open(self, fp):
        """open

        Keyword arguments:
        fp -- path file
        """
        self.infile = open(fp, 'rb')
        pass
    
    def __iter__(self):
        return self

    @staticmethod
    def read_header(data):
        type_alias, magic, clock1, clock2, clock3, clock4, clock5, clock6, label, load_size = struct.unpack(FasterFileReader._header_fmt, data)
        header = dict(zip(
                    "type_alias,magic,clock1,clock2,clock3,clock4,clock5,clock6,label,load_size".split(","),
                    map( int, [type_alias, magic, clock1, clock2, clock3, clock4, clock5, clock6, label, load_size])
                    ) )
        return header

    @staticmethod
    def read_data(src, head):
        data=""
        if head['load_size']>0:
            data = src.read(struct.calcsize('c'*(head['load_size']/2**8)))
        return data

    def next(self):
        """next() -> TNTEvent"""
        if ((self._nevent > self.maxnevents) and
            not self.maxnevents==-1):
            raise StopIteration
        head_data = self.infile.read(self._header_size)
        if not head_data:
            raise StopIteration
        else:
            self._nevent+=1
            header =  self.read_header(head_data)
            evt_data = self.read_data(self.infile, header)
            return FasterData(header, data=evt_data)
        pass #en
