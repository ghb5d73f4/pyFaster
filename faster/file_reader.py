#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:08:25 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: file_reader.py -*-
# -*- purpose: -*-
 
'''
Faster File reader

Imports
 - struct, 
 - faster.event
 - faster.const
'''

import struct 

# faster modules
import faster.event 
import faster.const 

class File_reader(object):
    """Stream FASTER events from file"""

    def __init__(self, evtfile="", maxnevents=faster.const.max_number_of_events_in_file):
        """Creator
        
        Keyword arguments:
        evtfile -- path to file to stream
        maxnevents -- number of events to read at most (default = -1 i.e. infinity
        """
        self.fpath = evtfile
        self.infile = None
        self.maxnevents = maxnevents
        self._nevent = 0
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
        #print(data.encode("hex"))
        type_alias,  magic, clock, label, load_size = struct.unpack(faster.const.header_fmt, data)
        # computing clock
        clock_words = struct.unpack(faster.const.clock_fmt, clock)
        time = sum([x*m for x,m in zip(clock_words,
                                       [1, 256, 65536, 16777216, 4294967296, 1099511627776])])
        return {    
            'type_alias': int(type_alias),
            'clock': time*faster.const.tick_ns,
            'magic': magic,
            'label': label,
            'load_size': load_size,
            }


    @staticmethod
    def read_data(src, head):
        return src.read(head['load_size'])#struct.calcsize("<"+str(head['load_size'])+'s'))

    def next(self):
        ''' for py2.7 compataibility'''
        return self.__next__()
        
    def __next__(self):
        """next() -> TNTEvent"""
        if (self._nevent >= self.maxnevents) :
            raise StopIteration
        head_data = self.infile.read(faster.const.header_size)
        if not head_data:
            raise StopIteration
        else:
            self._nevent+=1
            header =  self.read_header(head_data)
            evt_data = self.read_data(self.infile, header)
            return faster.event.Event(header, data=evt_data)
        pass #en
