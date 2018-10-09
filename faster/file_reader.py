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

_the_header_unpacker = struct.Struct(faster.const.header_fmt)

class File_reader(object):
    """Stream FASTER events from file"""

    def __init__(self, 
                 fasterfile="", 
                 maxnevents=faster.const.max_number_of_events_in_file):
        """Creator
        
        Keyword arguments:
        evtfile -- path to file to stream
        maxnevents -- number of events to read at most (default = -1 i.e. infinity
        """
        self.fpath = fasterfile
        self.infile = None
        self.maxnevents = maxnevents
        self._nevent = 0
        if (fasterfile!=""):
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
        ### ADD: checks of file exists and is file.
        self.infile = open(fp, 'rb')
        pass
    
    def __iter__(self):
        return self

    @staticmethod
    def _multiply(x,y):
        '''simple multiply function used for time calculation'''
        return x*y
    
    @staticmethod
    def read_header(data):
        '''Static method, unpacked a header from data'''
        #type_alias,  magic, clock[], label, load_size 
        updata = _the_header_unpacker.unpack(data)
        #print(updata)
        # computing clock
        time = sum(map(faster.File_reader._multiply,
                       updata[2:8],
                       faster.const.clock_multipliers))
        return {    
            'type_alias': updata[0],
            'clock': time,
            #'magic': updata[1], # magic is not useful
            'label': updata[-2],
            'load_size': updata[-1],
            }


    @staticmethod
    def read_data(src, head):
        ''' Return head[load_size] from the src'''
        return src.read(head['load_size'])

    def next(self):
        ''' for py2.7 compataibility'''
        return self.__next__()
        
    def __next__(self):
        """return next event in files, including data"""
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
