#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Thu May  4 15:40:35 CEST 2017 -*-
# -*- copyright: GH/IPHC 2017 -*-
# -*- file: histogram.py -*-
 
'''
Module for handling 1D histogram

An histogram is an ordered list of bins
'''


from pyhisto.bin import Bin

class Histogram(object):
    '''This class contains a list of 1D bins and provide interfaces to use them

    The Histogram has bins covering [xmin:xmax[
    '''

    def __init__(self,
                 nbins=1,
                 xmin=-0.5,
                 xmax=None,
                 fromstring=None,
                 frombins=None,
                 fromvalues=None,
                 fromdict=None):
        '''Initialize the histogram
        
        - Using a string (obtained from str) using 
        ``Histogram(fromstring=z)``

        - Using a list of bins (as in bins[x:y]) using
        ```Histogram(frombins=l)``

        - Using a dict (obtained from repr)
        ``Histogram(fromdicy=d)``
        
        - Using a list of values
        ``Histogram(fromvalues=l)``

        - Using the 'natural way'
        ``Histogram(nbins, xmin, xmax)``
        '''
        if fromstring:
            self._fromstring(fromstring)
            pass
        elif frombins:
            self._frombins(frombins)
        elif fromdict:
            self._fromdict(fromdict)
            pass
        elif fromvalues:
            self._fromvalues(fromvalues)
        else:
            self.nbins = nbins
            self.xmin = xmin
            self.xmax = xmax
            if xmax==None:
                self.xmax = xmin+nbins
            if self.xmax<self.xmin:
                self.xmin, self.xmax = min(self.xmin, self.xmax), max(self.xmin, self.xmax)
            self.binwidth=(self.xmax-self.xmin)/self.nbins
            self.bins = [Bin(self.xmin+i*self.binwidth,
                             self.binwidth) for i in range(self.nbins) ]
            self.outofrange = 0
        pass

    def __repr__(self):
        '''Represent the histogram as a dictionnary, list'''
        z=''
        z+="{{'nbins': {0}, 'xmin': {1}, 'xmax': {2}, 'oor': {3}, \n".format(self.nbins, 
                                                                        self.xmin,
                                                                        self.xmax,
                                                                        self.outofrange)
        z+="'bins': [ \n"
        for b in self.bins:
            z+="\t {0}, \n".format(repr(b))
        z+="        ]\n}"
        return z


    def __str__(self):
        '''Dump the histogram in string format'''
        z=''
        z+='# nbins = {0}\n'.format(self.nbins)
        z+='# xmin = {0}\n'.format(self.xmin)
        z+='# xmax = {0}\n'.format(self.xmax)
        for i in range(0, self.nbins):
            z+="{0} \n".format(str(self.bins[i]))
            pass
        z+='# out of range = {0}\n'.format(self.outofrange)
        return z
        #end for
    #end __str__

    def _fromstring(self, instr):
        '''This function imports an histogram from a string, 
        formatted as the output of __str__'''
        lines = instr.split('\n')
        for l in lines:
            if l.startswith("# nbins"):
                self.nbins = int(l.split('=')[1])
                self.bins = []
            elif l.startswith("# xmin"):
                self.xmin = float(l.split('=')[1])
            elif l.startswith("# xmax"):
                self.xmax = float(l.split('=')[1])
            elif l.startswith("# out of range"):
                self.outofrange = float(l.split('=')[1])
            elif l.startswith('#'): # any other commented line
                pass
            elif len(l)<=1:
                pass
            else:
                try:
                    self.bins.append(Bin(fromstring=l))
                except:
                    pass
                pass
            #end if
            pass
        #end for lines
        self.binwidth=(self.xmax-self.xmin)/self.nbins
    #end _fromstring

    def _frombins(self, bs):
        ''' This function imports an hisogram from a list of bins '''
        self.bins = sorted(bs, key=lambda x:x.lowedge)
        self.xmin = self.bins[0].lowedge #min(bs, key=lambda x:x.lowedge)
        self.xmax = self.bins[-1].upedge #max(bs, key=lambda x:x.upedge)
        self.nbins = len(bs)
        self.binwidth = self.bins[0].width()
        self.outofrange = 0

    def _fromvalues(self, lsv):
        ''' import from a list of values ''' 
        self.nbins = len(lsv)
        self.xmin = -0.5
        self.bins = []
        for i in range(self.nbins):
            self.bins.append(Bin(lowedge=i-0.5, width=1, count=lsv[i]))
        self.xmax = self.bins[-1].upedge
        self.binwidth = self.bins[0].width()
        self.outofrange = 0
        pass

            
    def _fromdict(self, json):
        raise NotImplementedError
        pass
    
    def todict(self):
        ''' Return a dictionnary like structure '''
        return eval(repr(self))


    ### Container like behavior
    def __getitem__(self, k):
        return self.bins[k]
    
    def __setitem__(self, k, v):
        self.bins[k]=v
        pass
    
    def __len__(self):
        return self.nbins

    def index(self, x):
        ''' Return the index corresponding to x (slow version)'''
        for i in range(len(self.bins)):
            if x in self.bins[i]:
                return i
            #end if
            pass
        #end for
        raise IndexError
        pass

    def find(self, x):
        ''' Return the bin corresponding to x (slow)'''
        for b in self.bins:
            if x in b:
                return b
            #end if
            pass
        #end for
        raise IndexError
        pass

    ##fast index uses xmin, width to go fast
    def fast_index(self, x):
        return int((x-self.xmin)/self.binwidth) #int rounds up with floor already!

        
    def slice(self, _from=None, to=None):
        #default from is first bin [:ito]
        ifrom = 0
        if _from:
            ifrom = self.index(_from)
        #default to is last bin [ifrom:]
        ito = self.nbins-1
        if to:
            ito = self.index(to)
        #return bins slice
        return Histogram(frombins=self.bins[ifrom:ito+1])
        pass

    def __iter__(self):
        ''' provides iteration over bin directly '''
        return iter(self.bins)

    def empty(self, who='all'):
        ''' Empty the counts from all bins '''
        if who=='all':
            for b in self.bins:
                b.count=0
                pass
            pass
        elif type(who)==list:
            for x in who:
                self.find(x).count=0
                pass
            pass
        else:
            self.find(who).count=0
        pass

    def copy(self):
        ''' Return a copy of the histogram '''
        return Histogram(fromstring=str(self))

    def empty_copy(self):
        ''' Return a new Histogram with the same xmax, xmin, ... but all counts to 0'''
        hout = self.copy()
        hout.empty()
        hout.outofrange = 0
        return hout
                    
    def fill(self, x, w=1):
        try:
            self.find(x).fill(w)
        except IndexError:
            self.outofrange+=w
            pass
        pass

        pass

    def fast_fill(self, x, w=1):
        try:
            self.bins[int((x-self.xmin)/self.binwidth)].fill(w)
        except IndexError:
            self.outofrange+=w
            pass
        pass
    
    def xy(self, x_pos='low'):
        return zip(*[b.xy(x_pos) for b in self.bins])
        pass

    ### scalar operations: add, sub, ul, divide
    def __iadd__(self, o):
        ''' Increment all bins by o if float or bin by bin if histogram '''
        if type(o)==Histogram:
            for b1,b2 in zip(self.bins, o.bins):
                b1+=b2
        else:
            for b in self.bins:
                b+=float(o)
        return self

    def __add__(self, o):
        ''' Return a new histogram with counts added '''
        newH = self.empty_copy()
        if type(o)==Histogram:
            for a,b1,b2 in zip(newH, self.bins, o.bins):
                a.count=b1.count+b2.count
        else:
            for a,b in zip(newH,self.bins):
                a.count=b.count+float(o)
        return newH
        
    def __radd__(self, o):
        ''' This type of operation makes no sense -> TypeError '''
        raise TypeError('Adding an histogram to something other than an histogram makes no sense' )

    def __isub__(self, o):
        ''' Decrement all bins by o if float or bin by bin if histogram '''
        if type(o)==Histogram:
            for b1,b2 in zip(self.bins, o.bins):
                b1-=b2
        else:
            for b in self.bins:
                b-=float(o)
        return self

    def __sub__(self, o):
        ''' Return a new histogram with counts substracted '''
        newH = self.empty_copy()
        if type(o)==Histogram:
            for a,b1,b2 in zip(newH, self.bins, o.bins):
                a.count=b1.count-b2.count
        else:
            for a,b in zip(newH,self.bins):
                a.count=b.count-float(o)
        return newH
        
    def __rsub__(self, o):
        ''' This type of operation makes no sense -> TypeError '''
        raise TypeError('Adding an histogram to something other than an histogram makes no sense' )
        
    def __imul__(self, o):
        ''' Multiply all bins by o if float or bin by bin if histogram '''
        if type(o)==Histogram:
            for b1,b2 in zip(self.bins, o.bins):
                b1*=b2
        else:
            for b in self.bins:
                b*=float(o)
        return self

    def __mul__(self, o):
        ''' Return a new histogram with counts multiplied '''
        newH = self.empty_copy()
        if type(o)==Histogram:
            for a,b1,b2 in zip(newH, self.bins, o.bins):
                a.count=b1.count*b2.count
        else:
            for a,b in zip(newH,self.bins):
                a.count=b.count*float(o)
        return newH
        
    def __rmul__(self, o):
        ''' This type of operation makes no sense -> TypeError '''
        raise TypeError('Adding an histogram to something other than an histogram makes no sense' )
        

    def __idiv__(self, o):
        ''' Divide all bins by o if float or bin by bin if histogram '''
        if type(o)==Histogram:
            for b1,b2 in zip(self.bins, o.bins):
                b1/=b2
        else:
            for b in self.bins:
                b/=float(o)
        return self

    def __div__(self, o):
        ''' Return a new histogram with counts divided '''
        newH = self.empty_copy()
        if type(o)==Histogram:
            for a,b1,b2 in zip(newH, self.bins, o.bins):
                a.count=b1.count/b2.count
        else:
            for a,b in zip(newH,self.bins):
                a.count=b.count/float(o)
        return newH
        
    def __rdiv__(self, o):
        ''' This type of operation makes no sense -> TypeError '''
        raise TypeError('Adding an histogram to something other than an histogram makes no sense' )
        
    def autocrop(self, 
                 mincount = 0.0,
                 minwidth = 1.0e-10):
        ''' Clean this histogram (returns self):
        - Remove bins on the side with less than mincount
        - Remove bins with width less than minwidth
        - Reorder bins according to xmin
        '''

        # remove null-width
        for b in self.bins:
            if b.width()<minwidth:
                #print("bin {0} is too small".format(b))
                self.bins.remove(b)
                pass
            pass
        #end for
        # scan up
        imin = 0
        for i in range(len(self.bins)):
            imin = i
            if self.bins[i].count>mincount:
                break
            pass
        #end for
        # scan down
        imax = self.nbins
        for i in reversed(range(len(self.bins))):
            imax = i+1
            if self.bins[i].count>mincount:
                break
            pass
        #end for
        # send to _frombins to make a proper histogram
        self._frombins(self.bins[imin:imax])
        return self
