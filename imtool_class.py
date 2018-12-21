# Classes and methods useful for imtools

import numpy as np
from astropy.io import fits as aiof
class header:
    maxdim = 10
    naxes = np.zeros(maxdim,dtype='int')
    crval = np.zeros(maxdim,dtype='float')
    cdelt = np.zeros(maxdim,dtype='float')
    crpix = np.zeros(maxdim,dtype='int')
    ctype = np.zeros(maxdim,dtype='U8')
    cunit = np.zeros(maxdim,dtype='U8')
    naxis = 1 
    simple = bool()
    bitpix = -32 
    datatype = np.float32
    restfreq = float()
    specsys = str()
    bmin = float()
    bmaj = float()
    bpa = int()
    btype = 'Intensity'
    bunit = str()
    bscale = 1.0
    bzero = 0.0
    #origin = str()
    timesys = 'UTC'
    date = str()
    
    # TODO: * Incoroporate a docstring for the function
    #       * Tools to generate document: sphinx, doxygen 
    def get(self,fitsfile,hduNum=0):
        if fitsfile == '':
            print 'file not specified'
            exit()
        else:
            f=aiof.open(fitsfile,mode='readonly')
        self.naxis = aiof.getval(fitsfile,'NAXIS')
        for iaxis in range(1,self.naxis+1):
            # Get the Naxis values:
            string = 'naxis'+str(iaxis)
            tmpnum = aiof.getval(fitsfile,string,ext=hduNum)
            self.naxes[iaxis] = tmpnum
        
            # Get the coordinate reference value: 
            string = 'crval'+str(iaxis)
            tmpnum = aiof.getval(fitsfile,string,ext=hduNum)
            self.crval[iaxis] = tmpnum
        
            # Get the coordinate reference pixel: 
            string = 'crpix'+str(iaxis)
            tmpnum = aiof.getval(fitsfile,string,ext=hduNum)
            self.crpix[iaxis] = tmpnum
        
            # Get the coordinate increment values: 
            string = 'cdelt'+str(iaxis)
            tmpnum = aiof.getval(fitsfile,string,ext=hduNum)
            self.cdelt[iaxis] = tmpnum
        
            # Get the Ctypes: 
            string = 'ctype'+str(iaxis)
            tmpstr = aiof.getval(fitsfile,string,ext=hduNum)
            self.ctype[iaxis] = tmpstr
        
            # Get the Units: 
            string = 'cunit'+str(iaxis)
            tmpstr = aiof.getval(fitsfile,string,ext=hduNum)
            self.cunit[iaxis] = tmpstr
        self.simple = aiof.getval(fitsfile,'SIMPLE')
        try:
            self.bitpix = aiof.getval(fitsfile,'BITPIX')
	    if self.bitpix == -32:
		    datatype = np.float32 
	except:
            print "bitpix NOT found, can't proceed..."
        self.restfreq = aiof.getval(fitsfile,'RESTFRQ')
        self.specsys = aiof.getval(fitsfile,'SPECSYS')
        self.bmin = aiof.getval(fitsfile,'BMIN')
        self.bmaj = aiof.getval(fitsfile,'BMAJ')
        self.bpa = aiof.getval(fitsfile,'BPA')
        self.btype = aiof.getval(fitsfile,'BTYPE')
        self.bunit = aiof.getval(fitsfile,'BUNIT')
        self.bzero = aiof.getval(fitsfile,'BZERO')
        self.bscale = aiof.getval(fitsfile,'BSCALE')
        self.timeSys = aiof.getval(fitsfile,'TIMESYS')
        #self.origin = aiof.getval(fitsfile,'ORIGIN')
        self.date = aiof.getval(fitsfile,'DATE')
        #Close the fits file
        f.close()
