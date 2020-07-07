import cdms2
import glob
import cdutil
import matplotlib 
import matplotlib.pyplot as plt

var = 'ua'
#var = 'tauv'
lev = 20000.

#lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2_clims/atmos/' + var + '/*/*.DJF.nc')

fjra = '/p/user_pub/pmp/pmp_obs_preparation/orig/data/JRA55-CREATEIP/CREATE-IP.MREreanalysis.JMA.JRA-55.CREATE-MRE.atmos.mon.v20200609.ua_Amon_MREreanalysis_JRA-55_1981.nc'

fera5 = '/p/user_pub/pmp/pmp_obs_preparation/orig/data/ERA5-CREATEIP/CREATE-IP.reanalysis.ECMWF.IFS-Cy41r2.ERA5.atmos.mon.v20200608.ua_Amon_reanalysis_ERA5_198201-198212.nc'

fera5_a = '/p/user_pub/PCMDIobs/PCMDIobs2_clims/atmos/ua/ERA-5/ua_mon_ERA-5_BE_1x1_197901-201812.v20200421.AC.nc'
fera5_a = '/p/user_pub/PCMDIobs/PCMDIobs2_clims/atmos/ua/ERA-5/ua_mon_ERA-5_BE_1x1_198901-198912.v20200610.AC.nc'

fera5_b = '/p/user_pub/PCMDIobs/PCMDIobs2/atmos/mon/ua/ERA-5/1x1/v20200402/ua_mon_ERA-5_BE_1x1_v20200402_198201-198212.nc'


lst = [fjra,fera5,fera5_a,fera5_b]
#lst = [fjra,fera5_a]



dic = {}

for l in lst:
  tmp1 = l.split('reanalysis_')
  print(tmp1)
  if l == fera5_a: print(l.split('_'))
# print(l.split('/'))
# var = l.split('/')[6]
  source = l.split('/')[7]
  if l == fera5_a: source = 'CLIM' 

  dic[source] = {}

  f = cdms2.open(l)
  d = f[var]
  try:
   t = d.getTime()
   tu = t.units
   c = t.asComponentTime()
   lc = len(c)
  except:
   pass

  ii = 0
  if l in [fera5]: ii = 1
  d0 = f(var) #,latitude = (-85.,85)) 
  d0 = d0(latitude = (0.,85.),time=slice(ii + 0,ii + 1))(squeeze=1)
  d0 = d0[::-1]

# units = d0.units
  lats = d0.getLatitude()[:]
  levs = d0.getLevel()[:]
  d0ga = cdutil.averager(d0,axis='xy')(squeeze=1)
  d0za = cdutil.averager(d0,axis='x')(squeeze=1)

# if len(d0.shape)==3 :
#    d0ga = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
#    d0za = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)

  try:
   d0NEX = d0(latitude=(40,60))
   d0gaNHEX = cdutil.averager(d0NEX,axis='xy')
  except:
   pass

  print(source,'--------')
  dic[source]={'levs' : levs,'gm' : d0ga.filled()}

  f.close()

  print(l)
# if len(d0.shape)==4 : print(list(d0ga(levels = (lev,lev))))
# if len(d0.shape)==2 : print(list(d0ga))

  try:
   print(c[0].year,'-', c[0].month,'   ', c[lc-1].year,'-',c[lc-1].month,'   ', tu)
   print(c[0:12])
  except:
   pass
  #print('T0 global average ', d0ga)
  print('------------------------------------------------------') 


fig, ax = plt.subplots()

leg = []
for src in list(dic.keys()):
 leg.append(src)

for src in list(dic.keys()):
 lat = dic[src]['levs']
 zm  = dic[src]['gm']

 ax.plot(zm, lat)

ax.set_xticks([-9., -6.,-3., 0,3.,6.,9.])
ax.set_xticklabels(['-9', '-6','-3', '0','3','6','9'])

ax.set_ylim(100000., 0) 

plt.legend(leg, loc='upper right')

ax.set(xlabel='Latitude', ylabel='bla',
       title= var)
ax.grid()

fig.savefig("test.png")
plt.show()



