import cdms2
import glob
import cdutil


lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2.0/atmos/mon/*/*/gn/v20200117/*.nc')

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

  f.close()

  print(l)
  print(c[0].year,'-', c[0].month,'   ', c[lc-1].year,'-',c[lc-1].month,'   ', tu)
  print(c[0:12])
  #print('T0 global average ', d0ga)
  print('------------------------------------------------------') 
