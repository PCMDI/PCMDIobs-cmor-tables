import cdms2
import glob
import cdutil


var = 'pr'
#var = 'tauv'

#lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2.0/atmos/mon/*/*/gn/v20200117/*.nc')
lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2.0-beta/atmos/mon/' + var + '/*/gn/*/*.nc')
lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2.0-beta/atmos/mon/' + var + '/*/gn/latest/*.nc')


for l in lst:
# print(l.split('/'))
  var = l.split('/')[7]

  f = cdms2.open(l)
  d = f[var]
  t = d.getTime()
  tu = t.units
  c = t.asComponentTime()
  lc = len(c)
  d0 = f(var,time=slice(0,1))
  d0ga = cdutil.averager(d0,axis='xy')

  try:
   d0NEX = d0(latitude=(40,60))
   d0gaNHEX = cdutil.averager(d0NEX,axis='xy')
  except:
   pass

  f.close()

  print(l,' ', float(d0ga))
  try:
   print(float(d0gaNHEX))
  except:
   pass
  print(c[0].year,'-', c[0].month,'   ', c[lc-1].year,'-',c[lc-1].month,'   ', tu)
  print(c[0:12])
  #print('T0 global average ', d0ga)
  print('------------------------------------------------------') 
