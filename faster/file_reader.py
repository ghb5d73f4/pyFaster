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
'''

import struct 

import event

class File_reader(object):
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
        type_alias, magic, clock1, clock2, clock3, clock4, clock5, clock6, label, load_size = struct.unpack(File_reader._header_fmt, data)
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
            return event.Event(header, data=evt_data)
        pass #en