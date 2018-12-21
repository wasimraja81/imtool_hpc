"""
This is a prototype for a HPC framework for performing 
operations on big-data (FITS images). In this example, 
the operation we choose is the computation of standard 
deviation along xy-planes for all z-values of the data 
cube. The data cube in this example is a FITS image 
with dimension (RA,Dec,Stokes,Frequency). 

* Only FITS images are considered in designing the prototype.
* The prototype does not care about the actual operation to 
  be performed on the data. 
* The prototype provides methods to:
    -- Read user-specified instructions (eg., input data, 
       dimensions across which to perform operations)
    -- Read metadata from the data files
    -- Interpret the meta-data and the user-specified params 
       to decide on the work distribution amongst available 
       processes (CPUs). Let's look at a few possible example 
       cases to illustrate the complexity involved in 
       interpretation:
       ++ Finding the mean of all pixels in the xy-plane for 
          any given z in a FITS image sorted in xyzp order.
       ++ Finding the rms along z-dimension for all pixels in 
          xy-plane in a FITS image sorted in xypz order.
       ++ One of the above with Input FITS image WITHOUT the 
          p-dimension
* perform the desired operation using system functions or 
  user-defined functions.
* Out of scope: Optimising the functions used for the intended 
  operations
* Use cases:
    -- Routine operations requiring data validation and image 
       quality analysis
    -- Pipeline tasks such as image based continuum subtraction. 
       Implementation within non-HPC framework takes 12+ hours 
       for fitting and removing smooth trends (using polynomial 
       fits) for nominal data sizes from ASKAP28.
    -- Post processing of the images: compute rms map, meanMap, 
       spectralIndices
    -- More sophisticated image-processing – RM-synthesis for 
       example.

AUTHORS: Wasim.Raja@csiro.au
         Mohsin.Shaikh@csiro.au 
"""

from mpi4py import MPI
import numpy as np 
from astropy.io import fits as aiof

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


import imtool_class as imc
h = imc.header()
fitsfile='images/sn1006.bm25.fits'
h.get(fitsfile)
print "naxis: ",h.naxis
print "naxes: ",h.naxes


h.naxes
""" 
As of now, the nPix for the dimensions are extracted 
from prior knowledge of the dtaa structure in the FITS file. 
TODO: Derive the structure from the FITS header. 
"""
nx = h.naxes[1]
ny = h.naxes[2]
nz = h.naxes[4]
nworker = comm.Get_size()
nChan_per_worker = (int)(np.floor(nz/nworker))
nChan_remain = nz%nworker
if rank == nworker-1:
    e = (rank+1)*nChan_per_worker + nChan_remain
else:
    e = (rank+1)*nChan_per_worker
s = rank*nChan_per_worker


# Function to compute the rms of an image: we use numpy array here.
def imrms_np(fitsfile,s,e,stoke,dim=0,hduNumber=0):
    f = aiof.open(fitsfile,mode='readonly')
    im = f[hduNumber].section[s:e,stoke,:,:] 
    #im = f[hduNumber].section[:,:,s:e] 
    """ Close the fits file and 
    call the function for the computation"""
    f.close()
    rms = np.zeros(e-s,dtype=h.datatype)
    #print "Channels analysed:",s,"-",e
    for ichan in range(0,e-s):
        rms[ichan] = np.rms(im[ichan,stoke,:,:])
        #rms[ichan] = np.rms(im[:,:,ichan])
    return rms



tstart = MPI.Wtime()
#Code 
stoke=0
rms = np.zeros(e-s,dtype=h.datatype)
rms = imrms_np(fitsfile,s,e,stoke,0,0)
# Gather 
rms_arr = None
if rank == 0:
    rms_arr = np.zeros(nz,dtype=h.datatype)
comm.Gather(rms,rms_arr,root=0)
# Reduce
tend = MPI.Wtime()
print tend - tstart
print rms_arr
