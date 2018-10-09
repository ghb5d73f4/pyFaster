#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Oct  9 11:31:54 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: lazy_histogram.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''


class LazyHistogram(object):
    '''
    This Histogram is a liteweight version of 1D histo, for purpose of filling
    '''
    def __init__(self,
                 nbins=1,
                 xmin=-0.5,
                 xmax=None):
        self.nbins = nbins
        self.xmin = xmin
        self.xmax = xmax
        if xmax==None:
            self.xmax = xmin+nbins
        if self.xmax<self.xmin:
            self.xmin, self.xmax = min(self.xmin, self.xmax), max(self.xmin, self.xmax)
        self.binwidth=(self.xmax-self.xmin)/self.nbins
        self.bins = [0] * self.nbins
        self.outofrange = 0
        pass


    def __str__(self):
        '''Dump the histogram in string format'''
        z=''
        z+='# nbins = {0}\n'.format(self.nbins)
        z+='# xmin = {0}\n'.format(self.xmin)
        z+='# xmax = {0}\n'.format(self.xmax)
        for i in range(0, self.nbins):
            lowedge=self.xmin+i*self.binwidth
            z+="{0} {1} {2}\n".format(lowedge,
                                      self.binwidth,
                                      self.bins[i])
            pass
        z+='# out of range = {0}\n'.format(self.outofrange)
        return z
        #end for
    #end __str__

    ### Container like behavior
    def __getitem__(self, k):
        return self.bins[k]
    
    def __setitem__(self, k, v):
        self.bins[k]=v
        pass
    
    def __len__(self):
        return len(self.nbins)

    def fast_index(self, x):
        return int((x-self.xmin)/self.binwidth) #int rounds up with floor already!

    def __iter__(self):
        ''' provides iteration over bin directly '''
        return iter(self.bins)
    
    def fast_fill(self, x, w=1):
        try:
            self.bins[int((x-self.xmin)/self.binwidth)]+=w
        except IndexError:
            self.outofrange+=w
            pass
        pass
