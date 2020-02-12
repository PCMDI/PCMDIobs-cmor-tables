import cdms2
import glob
import os
from regrid2 import Regridder

dbver = 'PCMDIobs2.0-beta'
ver = 'v20200206'
target = '1x1'

pin = '/p/user_pub/PCMDIobs/' + dbver + '/atmos/mon/*/CERES-EBAF-4-1/gn/' + ver + '/'
pin = '/p/user_pub/PCMDIobs/' + dbver + '/atmos/mon/ua/ERA-5/gn/' + ver + '/'

lst = glob.glob(pin + '*.nc')

# TARGET 1x1 grid

fit = '/p/user_pub/PCMDIobs/PCMDIobs1.0/atm/mo/rlut/CERES/ac/rlut_CERES_000001-000012_ac.nc'
fo = cdms2.open(fit)
do = fo['rlut']
tgrid = do.getGrid()


for l in lst:   #[0:2]:
#print(l)

 newfile = l.replace('gn',target)
 newdir_tmp = newfile.split('/')[0:9]  
 var = newfile.split('/')[7] 
 rep = '/'
 newdir = rep.join(newdir_tmp)
#print(newdir)

 try:
  os.mkdir(newdir + '/' + target)
 except:
  print('cant make dir ' + newdir + '/' + target)

 try:
  os.mkdir(newdir + '/' + target + '/' + ver + '/')
 except:
  pass


 fc = cdms2.open(l)
 d = fc(var)
 orig_grid = d.getGrid()

 regridFunc = Regridder(orig_grid,tgrid)

 dn = regridFunc(d)
 dn.id = var

 g = cdms2.open(newfile,'w+')
 g.write(dn)
 g.close()

#print(newdir)
 print('done with ', newfile)

