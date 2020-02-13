import os, sys
import glob

# MAPS PCMDIObs FROM BY VARIABLE TO BY SOURCE VIA SYMBOLIC LINKS

base_dir = '/p/user_pub/PCMDIobs/'
data_ver = 'PCMDIobs2.0-beta'
root = base_dir + '/' + data_ver + '/'

try:
 new_root = root +'bySource'
 os.mkdir(new_root)
except:
 pass

lst = glob.glob(root + '*/*/*/*/*/*/*.nc')
products = []
for l in lst: 
  p = l.split('/')[9]
  if p not in products: products.append(p)

try:
  os.mkdir(new_root)
except:
  pass

for p in products:
 try:
  os.mkdir(new_root + '/' + p)
 except:
  pass

 pp= root + '*/*/*/' + p + '/*/*/*.nc'
 lstp = glob.glob(pp)
 print(p,' ', len(lstp))

 for l in lstp:
   fn = l.split('/')[12]

   os.symlink(l,new_root + '/' + p + '/' + fn)
