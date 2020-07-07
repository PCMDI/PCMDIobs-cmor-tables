import cdms2
import glob
import cdutil
import matplotlib 
import matplotlib.pyplot as plt

var = 'ua'
lev = 20000.
#lev = 85000.
#lev = 50000.
zm_month = 1

llat = 30.
ulat = 60.
mod1 = 'E3SM-1-0'
mod2 = 'CESM2'
#mod2 = 'ACCESS-CM2'

t = [1,2,3,4,5,6,7,8,9,10,11,12]

lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2_clims/atmos/' + var + '/*/*.AC.nc')

# Two models 
modpath = '/p/user_pub/pmp/pmp_results/pmp_v1.1.2/diagnostic_results/CMIP_CLIMS/cmip6/historical/v20200526/'
fm1 = cdms2.open(modpath + var + '/' + 'cmip6.historical.' + mod1 + '.r1i1p1f1.mon.' + var + '.198101-200512.AC.v20200526.nc')
dm1 = fm1(var,latitude = (llat,ulat))
lats1 = dm1.getLatitude()[:]
#dm1 = dm1(latitude = (llat,ulat))

fm2 = cdms2.open(modpath + var + '/' + 'cmip6.historical.' + mod2 + '.r1i1p1f1.mon.' + var + '.198101-200512.AC.v20200526.nc')
dm2 = fm2(var,latitude = (llat,ulat))
lats2 = dm2.getLatitude()[:]
#dm2 = dm2(latitude = (llat,ulat))

dic = {}
dic['ts'] = {}
dic['zm'] = {}
dic['ts'][mod1] = {}
dic['ts'][mod2] = {}
dic['zm'][mod1] = {}
dic['zm'][mod2] = {}

# MODEL RESULT
dmga1= cdutil.averager(dm1,axis='xy')(squeeze=1)
dmza1= cdutil.averager(dm1,axis='x')(squeeze=1)
if len(dm1.shape)==4 :
     dmga1 = cdutil.averager(dm1(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     dmza1= cdutil.averager(dm1(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)
dic['ts'][mod1]={'mo' : t,'tm' : dmga1.filled()}
dic['zm'][mod1]={'lat' : lats1,'zm' : dmza1[zm_month].filled()}


dmga2= cdutil.averager(dm2,axis='xy')(squeeze=1)
dmza2= cdutil.averager(dm2,axis='x')(squeeze=1)
if len(dm2.shape)==4 :
     dmga2 = cdutil.averager(dm2(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     dmza2= cdutil.averager(dm2(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)
dic['ts'][mod2]={'mo' : t,'tm' : dmga2.filled()}
dic['zm'][mod2]={'lat' : lats2,'zm' : dmza2[zm_month].filled()}

for l in lst:
# print(l.split('/'))
  var = l.split('/')[6]
  source = l.split('/')[7] + '_' + l.split('.')[1]
  if source !='TropFlux-1-0': 
   dic['ts'][source] = {}
#  dic['zm'][source] = {}

  f = cdms2.open(l)
  d = f[var]
  try:
#  t = d.getTime()
   tu = t.units
   c = t.asComponentTime()
   lc = len(c)
  except:
   pass

  d0 = f(var,latitude = (llat,ulat)) 
  latsm = d0.getLatitude()[:] 
# units = d0.units
# lats = d0.getLatitude()[:]
  d0ga = cdutil.averager(d0,axis='xy')(squeeze=1)
  d0za = cdutil.averager(d0,axis='x')(squeeze=1)
  if len(d0.shape)==4 :
     d0ga = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     d0za = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)

  if source !='TropFlux-1-0':  
   print(source,'--------')
   dic['ts'][source]={'mo' : t,'tm' : d0ga.filled()}
   dic['zm'][source]={'lat' : latsm,'zm' : d0za[zm_month].filled()}


  f.close()
  print(l)

  try:
   print(c[0].year,'-', c[0].month,'   ', c[lc-1].year,'-',c[lc-1].month,'   ', tu)
   print(c[0:12])
  except:
   pass
  #print('T0 global average ', d0ga)
  print('------------------------------------------------------') 

#### TIME SERIES PLOT
fig, ax = plt.subplots()
leg = []
for src in list(dic['ts'].keys()):
 leg.append(src)

for src in list(dic['ts'].keys()):
 reg_avg = dic['ts'][src]['mo']
 t_ax  = dic['ts'][src]['tm']
 ax.plot(reg_avg, t_ax)

ax.set_xticks(t)
ax.set_xticklabels(['D','J','F','M','A','M','J','J','A','S','O','N','D'])
ax.set(xlabel='Latitude', ylabel='bla', title= var)
ax.grid()
plt.legend(leg, loc='upper right')
fig.savefig(var + "tseries.png")
#plt.show()

print('TS done')

### ZONAL MEAN OF DEC
fig, ax = plt.subplots()

leg = []
for src in list(dic['zm'].keys()):
 leg.append(src)

for src in list(dic['zm'].keys()):
 lat = dic['zm'][src]['lat']
 zm  = dic['zm'][src]['zm']

 ax.plot(lat, zm)

ax.set_xticks([-90., -60.,-30., 0,30.,60.,90.])
ax.set_xticklabels(['-90', '-60','-30', '0','30','60','90'])

plt.legend(leg, loc='upper right')

ax.set(xlabel='Latitude', ylabel='bla', title= var)
ax.grid()

fig.savefig(var + "zm-dec.png")
plt.show()

print('DONE')
