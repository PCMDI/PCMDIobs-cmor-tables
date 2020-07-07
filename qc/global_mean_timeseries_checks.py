import cdms2
import glob
import cdutil
import matplotlib 
import matplotlib.pyplot as plt

var = 'ua'
lev = 20000.
#lev = 85000.

llat = 0.
ulat = 90.
mod1 = 'E3SM-1-0'
mod2 = 'CESM2'

t = [1,2,3,4,5,6,7,8,9,10,11,12]

lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2_clims/atmos/' + var + '/*/*.AC.nc')

# Two models 
modpath = '/p/user_pub/pmp/pmp_results/pmp_v1.1.2/diagnostic_results/CMIP_CLIMS/cmip6/historical/v20200526/'
fm1 = cdms2.open(modpath + var + '/' + 'cmip6.historical.' + mod1 + '.r1i1p1f1.mon.' + var + '.198101-200512.AC.v20200526.nc')
dm1 = fm1(var,latitude = (llat,ulat))

fm2 = cdms2.open(modpath + var + '/' + 'cmip6.historical.' + mod2 + '.r1i1p1f1.mon.' + var + '.198101-200512.AC.v20200526.nc')
dm2 = fm2(var,latitude = (llat,ulat))

dic = {}

dic[mod1] = {}
dic[mod2] = {}

# MODEL RESULT
dmga1= cdutil.averager(dm1,axis='xy')(squeeze=1)
dmza1= cdutil.averager(dm1,axis='x')(squeeze=1)
if len(dm1.shape)==4 :
     dmga1 = cdutil.averager(dm1(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     dmza1= cdutil.averager(dm1(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)
dic[mod1]={'mo' : t,'tm' : dmga1.filled()}

dmga2= cdutil.averager(dm2,axis='xy')(squeeze=1)
dmza2= cdutil.averager(dm2,axis='x')(squeeze=1)
if len(dm2.shape)==4 :
     dmga2 = cdutil.averager(dm2(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     dmza2= cdutil.averager(dm2(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)
dic[mod2]={'mo' : t,'tm' : dmga2.filled()}

for l in lst:
# print(l.split('/'))
  var = l.split('/')[6]
  source = l.split('/')[7]
  if source !='TropFlux-1-0': dic[source] = {}

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
# units = d0.units
# lats = d0.getLatitude()[:]
  d0ga = cdutil.averager(d0,axis='xy')(squeeze=1)
  d0za = cdutil.averager(d0,axis='x')(squeeze=1)
  if len(d0.shape)==4 :
     d0ga = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     d0za = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)

  if source !='TropFlux-1-0':  
   print(source,'--------')
   dic[source]={'mo' : t,'tm' : d0ga.filled()}

  f.close()
  print(l)

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
 reg_avg = dic[src]['mo']
 t_ax  = dic[src]['tm']
 ax.plot(reg_avg, t_ax)

ax.set_xticks(t)
ax.set_xticklabels(['D','J','F','M','A','M','J','J','A','S','O','N','D'])

plt.legend(leg, loc='upper right')

ax.set(xlabel='Latitude', ylabel='bla',
       title= var)
ax.grid()

fig.savefig("test.png")
plt.show()



