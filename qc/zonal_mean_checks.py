import cdms2
import glob
import cdutil
import matplotlib 
import matplotlib.pyplot as plt

var = 'ta'
#var = 'tauv'
lev = 20000.

lst = glob.glob('/p/user_pub/PCMDIobs/PCMDIobs2_clims/atmos/' + var + '/*/*.DJF.nc')

dic = {}

for l in lst:
# print(l.split('/'))
  var = l.split('/')[6]
  source = l.split('/')[7]

  if source !='TropFlux-1-0': dic[source] = {}

  f = cdms2.open(l)
  d = f[var]
  try:
   t = d.getTime()
   tu = t.units
   c = t.asComponentTime()
   lc = len(c)
  except:
   pass

  d0 = f(var) #,latitude = (-85.,85)) 
  d0 = d0(latitude = (-55.,55.))
# units = d0.units
  lats = d0.getLatitude()[:]
  d0ga = cdutil.averager(d0,axis='xy')(squeeze=1)
  d0za = cdutil.averager(d0,axis='x')(squeeze=1)

  if len(d0.shape)==3 :
     d0ga = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='xy')(squeeze=1)
     d0za = cdutil.averager(d0(levels = (lev,lev))(squeeze=1),axis='x')(squeeze=1)

  try:
   d0NEX = d0(latitude=(40,60))
   d0gaNHEX = cdutil.averager(d0NEX,axis='xy')
  except:
   pass

  if source !='TropFlux-1-0':  
   print(source,'--------')
   dic[source]={'lat' : lats,'zm' : d0za.filled()}

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
 lat = dic[src]['lat']
 zm  = dic[src]['zm']

 ax.plot(lat, zm)

ax.set_xticks([-90., -60.,-30., 0,30.,60.,90.])
ax.set_xticklabels(['-90', '-60','-30', '0','30','60','90'])

plt.legend(leg, loc='upper right')

ax.set(xlabel='Latitude', ylabel='bla',
       title= var)
ax.grid()

fig.savefig("test.png")
plt.show()



