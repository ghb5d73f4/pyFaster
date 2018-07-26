#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Aug 11 10:22:50 CEST 2017 -*-
# -*- copyright: GH/IPHC 2017 -*-
# -*- file: histogram2D.py -*-
# -*- purpose: -*-
 
'''
The module contain the Histogram2D class.
'''

# importing 1D histogram to export projections
from pyhisto.histogram import Histogram

from math import floor,ceil,exp
#from pprint import pformat

class Histo2DError(Exception):
    '''2D Histogram error '''
    pass

class Histogram2D(object):
    ''' Implement 2D hisotgram'''

    def __init__(self,
                 xnbins=1, xmin=None, xmax=None, 
                 ynbins=1, ymin=None, ymax=None,
                 fromstring=None,
                 fromarray=None,
                 fromdict=None):
        '''Initilize the Hisotgram2D
        
        - Using a string, as exported from str(histo2d) using 
        ``Histogram2D(fromstring=z)``

        - Using a dictionnary, as obtained from repr, using
        ``Histogram2D(fromdict=d)``

        - Using an array of values, which will be indexed naturally, 
        ``Histogram2D(fromarray=a)``

        - From 'nothing', using
        ``Histogram2D(nxbins, xmin, xmax, nybins, ymin, ymax)``
        '''
        if fromstring:
            self._fromstring(fromstring)
        elif fromarray:
            pass
        elif fromdict:
            pass
        else:
            self.xnbins=xnbins
            self.ynbins=ynbins
            if(xmin==None):
                xmin = -0.5
            if(xmax==None):
                xmax = xmin+xnbins
            if(ymin==None):
                ymin = -0.5
            if(ymax==None):
                ymax = ymin+ynbins
            if (xmin==xmax):
                raise Histo2DError("X Bounds values in histogram should be different")
            if (ymin==ymax):
                raise Histo2DError("Y Bounds values in histogram should be different")
            xmin, xmax = min(xmax, xmin), max(xmax,xmin)
            ymin, ymax = min(ymax, ymin), max(ymax,ymin)
            self.xmin=xmin
            self.xmax=xmax
            self.xbinwidth=(self.xmax-self.xmin)/float(self.xnbins)
            self.ymin=ymin
            self.ymax=ymax
            self.ybinwidth=(self.ymax-self.ymin)/float(self.ynbins)
            self.bins = [[ 0  for j in range(self.ynbins) ] 
                               for i in range(self.xnbins)]
            self.outofrange = 0
            self.export_threshold = 0. # fine tune parameter
            pass
        #end if
        pass
    #end __init__

    def _fromstring(self, instr):
        '''This function imports an histogram from a string, 
        formatted as the output of __str__'''
        #print("### Calling fromstring with :"+instr)
        lines = instr.split('\n')
        for l in lines:
            #print("#Reading:"+l)
            if l.startswith("# xnbins"):
                self.xnbins = int(l.split('=')[1])
            elif l.startswith("# xmin"):
                self.xmin = float(l.split('=')[1])
            elif l.startswith("# xmax"):
                self.xmax = float(l.split('=')[1])
            elif l.startswith("# ynbins"):
                self.ynbins = int(l.split('=')[1])
                self.bins = [[ 0  for j in range(self.ynbins) ] for i in range(self.xnbins)]
            elif l.startswith("# ymin"):
                self.ymin = float(l.split('=')[1])
            elif l.startswith("# ymax"):
                self.ymax = float(l.split('=')[1])
            elif l.startswith("# out of range"):
                self.outofrange = float(l.split('=')[1])
            else:
                #print("#is '"+l+"' a data line ?")
                if (len(l.split())==3):
                    try:
                        i, j, c = map(None, l.split())
                        i, j, c = int(i), int(j), float(c)
                        #print("#adding {0} at {1}, {2}".format(c, i, j))
                        self.bins[i][j]=c
                    except:
                        pass
                pass
            #end if
            pass
        #end for lines
        self.xbinwidth=(self.xmax-self.xmin)/float(self.xnbins)
        self.ybinwidth=(self.ymax-self.ymin)/float(self.ynbins)
        pass #end _fromstring

    def __str__(self):
        '''Dump the histogram in string format'''
        z=''
        z+='# xnbins = {0}\n'.format(self.xnbins)
        z+='# xmin = {0}\n'.format(self.xmin)
        z+='# xmax = {0}\n'.format(self.xmax)
        z+='# ynbins = {0}\n'.format(self.ynbins)
        z+='# ymin = {0}\n'.format(self.ymin)
        z+='# ymax = {0}\n'.format(self.ymax)
        if (self.export_threshold>0.):
            z+='# Exporting bins with more than {0} counts\n'.format(self.export_threshold)
        for i in xrange(0, self.xnbins):
            for j in xrange(0, self.ynbins):
                if self.bins[i][j]>self.export_threshold:
                    z+="{0} {1} {2} \n".format(i, j, self.bins[i][j])
                pass
        z+='# out of range = {0}\n'.format(self.outofrange)
        return z
        #end for
    #end __str__


    def __repr__(self):
        '''Writting the histogram2D as a dictionnary'''
        z="{{ # {0}.{1} object at {2}\n".format(self.__class__.__module__,
                                               self.__class__.__name__,
                                               hex(id(self)))
        z+="   'xnbins':{0},\n".format(self.xnbins)
        z+="   'xmin':{0},\n".format(self.xmin)
        z+="   'xmax':{0},\n".format(self.xmax)
        z+="   'ynbins':{0},\n".format(self.ynbins)
        z+="   'ymin':{0},\n".format(self.ymin)
        z+="   'ymax':{0},\n".format(self.ymax)
        z+="   'outofrange':{0},\n".format(self.outofrange)
        z+="   'bins':{0},\n".format(str(self.bins))
        z+="}"
        return z
        #end for
    #end __repr__

    def todict(self):
        return eval(repr(self))

    def copy(self):
        '''Return a copy of the histogram'''
        return Histogram2D(fromstring=str(self))
        
    
    def empty(self):
        '''Sets all bin content to 0'''
        self.outofrange=0
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                self.bins[i][j]=0
                pass
            #end for j
            pass
        #end for i
        pass
    
    def empty_copy(self):
        '''Returns an empty copy (i.e. preserved just the axis)'''
        newh = self.copy()
        newh.empty()
        return newh

    def rescale(self, newxmin=None, newxmax=None,
                newymin=None, newymax=None):
        '''Change the scale, compute new bin width, ....'''
        if newxmin is not None:
            self.xmin = newxmin
        if newxmax is not None:
            self.xmax = newxmax
        if newymin is not None:
            self.ymin = newymin
        if newymax is not None:
            self.ymax = newymax
        self.xbinwidth=(self.xmax-self.xmin)/float(self.xnbins)
        self.ybinwidth=(self.ymax-self.ymin)/float(self.ynbins)
        pass


    def dim(self):
        '''Alternative to len, for 2D'''
        return self.xnbins, self.ynbins

    def sum(self):
        '''compute the sum, because sum() does not work on 2D'''
        S=0.0
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                S+= self.bins[i][j]
                pass
            #end for j
            pass
        #end for i
        return S

    def max(self):
       ' ''return position and value of maximum'''
       the_i, the_j, the_max = 0, 0, 0.0
       for i in range(self.xnbins):
           for j in range(self.ynbins):
               if self.bins[i][j] > the_max :
                   the_i, the_j, the_max = i, j, self.bins[i][j]
                   pass
                #end if
               pass
            #end for j
           pass
        #end for i
       return {'i': the_i, 'j': the_j, 'max': the_max}

    def scale(self, S=1.):
        '''Mutliply the content by S'''
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                self.bins[i][j]*=S
                pass
            #end for j
            pass
        #end for i

    def getbin(self, x, y):
        i,j = self.findbin(x,y)
        return {'i': i, 'j': j,
                'x': x, 'y': y,
                'lowedge': self.getbinlowedge(i,j),
                'updedge': self.getbinupedge(i,j),
                'count': self.bins[i][j]}

    def findbin(self, x, y):
        i, j = -1, -1
        if (x>= self.xmin and x<=self.xmax):
            i = int(floor((x-self.xmin)/self.xbinwidth))
            pass
        if (y>=self.ymin and y<=self.ymax):
            j =  int(floor((y-self.ymin)/self.ybinwidth))
            pass
        return i,j
    #end FindBin

    def fill(self, x, y, w=1.):
        '''Add one (or w) counts to bin corresponding to x

        Keyword Arguments:
        x,y -- (float)
        w -- (float) default =1'''
        i,j = self.findbin(x,y)
        if (i>=0 and j>=0):
            #
            try :
                self.bins[i][j]+=w
            except IndexError:
                self.outofrange+=w
            pass
        else:
            self.outofrange+=w
        pass
    # End Fill

    def fast_fill(self, x, y, w=1):
        '''Add one (or w) counts to the bin, in a fast way'''
        try:
            self.bins[int((x-self.xmin)/self.xbinwidth)][int((y-self.ymin)/self.ybinwidth)]+=w
        except IndexError:
            self.outofrange+=w
            pass
        pass

    def very_fast_fill(self, i, j, w=1):
        ''' add one (or w) counts to the bin identified with i,j'''
        try:
            self.bins[i][j]+=w
        except IndexError:
            self.outofrange+=w
        pass


    def getbincenter(self, i, j):
        return self.xmin+(i+0.5)*self.xbinwidth, self.ymin+(j+0.5)*self.ybinwidth
    
    def getbinlowedge(self, i, j):
        return self.xmin+(i)*self.xbinwidth, self.ymin+(j)*self.ybinwidth

    def getbinupedge(self, i, j):
        return self.xmin+(i+1.)*self.xbinwidth, self.ymin+(j+1.)*self.ybinwidth

 
    def xyz(self, mode='lowedge'):
        X = [ self.getbinlowedge(i, 0)[0]  for i in range(self.xnbins+1)]
        Y = [ self.getbinlowedge(0, j)[1]  for j in range(self.ynbins+1)]
        Z = zip(*self.bins)
        return X, Y, Z
        pass


    def project_x(self, ymin=-1, ymax=-1):
        '''project the histogram content on the X axis'''
        jmin = self.findbin(self.xmin, ymin)[1]
        jmax = self.findbin(self.xmin, ymax)[1]
        if ymin==-1:
            jmin = 0
        if ymax==-1:
            jmax = self.ynbins
        #print("#Projecting from bins {0} to {1}".format(jmin, jmax))
        d= [ sum([ self.bins[i][j] for j in xrange(jmin, jmax)]) for i in range(self.xnbins)]
        h = Histogram(self.xnbins, self.xmin, self.xmax)
        for i in range(self.xnbins):
            h.bins[i].count+=d[i]
            pass
        return h

    def project_y(self, xmin=-1, xmax=-1):
        '''project the histogram content on the X axis'''
        imin = self.findbin(xmin, self.ymin)[0]
        imax = self.findbin(xmax, self.ymin)[0]
        if xmin==-1:
            imin = 0
        if xmax==-1:
            imax = self.xnbins
        #print("#Projecting from bins {0} to {1}".format(imin, imax))
        d= [ sum([ self.bins[i][j] for i in xrange(imin, imax)]) for j in range(self.ynbins)]
        h = Histogram(self.ynbins, self.ymin, self.ymax)
        for j in range(self.ynbins):
            h.bins[j].count+=d[j]
            pass
        return h


    def rebin(self, newbinx=-1, newbiny=-1):
        '''Return a new histogram with same limits but different number of bins'''
        if newbinx==-1:
            newbinx = self.xnbins
        if newbiny==-1:
            newbiny = self.ynbins
        #
        rh = Histogram2D(newbinx,
                         self.xmin, self.xmax,
                         newbiny,
                         self.ymin, self.ymax)
        # Now filling the new histogram!
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                x, y = self.getbincenter(i, j)
                rh.fill(x, y, self.bins[i][j])
        #
        # 
        return rh


    def subhisto(self, xmin=-1, xmax=-1,
                 ymin=-1, ymax=-1):
        '''Return a new 2D histogram, with only the selected range'''
        # First, select
        jmin = self.findbin(self.xmin, ymin)[1]
        jmax = self.findbin(self.xmin, ymax)[1]
        imin = self.findbin(xmin, self.ymin)[0]
        imax = self.findbin(xmax, self.ymin)[0]
        if xmin==-1:
            imin = 0
        if xmax==-1:
            imax = self.xnbins
        if ymin==-1:
            jmin = 0
        if ymax==-1:
            jmax = self.ynbins
            pass
        jmin, jmax = min(jmin, jmax), max(jmin, jmax)
        imin, imax = min(imin, imax), max(imin, imax)
        #print("# Creating subdir from i={0}, j={1} to i={2}, j={3}".format(imin, jmin, imax, jmax))
        #then, creat ne histogram:
        subh = Histogram2D(imax-imin,
                           self.getbinlowedge(imin, jmin)[0], 
                           self.getbinlowedge(imax, jmin)[0],
                           jmax-jmin,
                           self.getbinlowedge(imin, jmin)[1], 
                           self.getbinlowedge(imin, jmax)[1])
        subh.bins = [ [ self.bins[i][j] for j in range(jmin,jmax)] 
                      for i in range(imin,imax) ]
        return subh


    def autocrop(self, threshold=0):
        '''Cut the bins that are 'empty' '''
        # Find the first i,j that is above threshold
        #use specialized function:
        def _ifromthetop():
            for i in xrange(self.xnbins):
                for j in xrange(self.ynbins):
                    if self.bins[i][j] > threshold :
                        return i
        def _jfromthetop():
            for j in xrange(self.ynbins):
                for i in xrange(self.xnbins):
                    if self.bins[i][j] > threshold :
                        return j
        def _ifromthebottom():
            for i in xrange(self.xnbins-1, 0, -1):
                for j in xrange(self.ynbins-1, 0, -1):
                    if self.bins[i][j] > threshold :
                        return i
        def _jfromthebottom():
            for j in xrange(self.ynbins-1, 0, -1):
                for i in xrange(self.xnbins-1, 0, -1):
                    if self.bins[i][j] > threshold :
                        return j
        i_top, j_top = _ifromthetop(), _jfromthetop()
        i_bot, j_bot = _ifromthebottom(), _jfromthebottom()
        i_top, i_bot = max(i_top, i_bot), min(i_top, i_bot)
        j_top, j_bot = max(j_top, j_bot), min(j_top, j_bot)
        xmin, ymin = self.getbinlowedge(i_bot, j_bot)
        xmax, ymax = self.getbinupedge(i_top, j_top)
        #print("# Autocropping from i={0}, j={1} to i={2}, j={3}".format(i_top, j_top, i_bot, j_bot))
        return self.subhisto(xmin, xmax, ymin, ymax)

 
