import cdms2
import glob

dbver = 'PCMDIobs2.0-tmp'
ver = 'v20200206'

pin = '/p/user_pub/PCMDIobs/' + dbver + '/atmos/mon/*/ERA-5/gn/' + ver + '/'

lst = glob.glob(pin)
