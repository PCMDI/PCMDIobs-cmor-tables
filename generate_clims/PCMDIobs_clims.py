import glob, os,sys
import cdms2, MV2
import cdutil
import datetime

ver = datetime.datetime.now().strftime('v%Y%m%d')
cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)

################################
seperate_clims = 'y' # 'y'
#################################

pin = '/p/user_pub/PCMDIobs/PCMDIobs2.0-beta/atmos/mon/'
pin = '/p/user_pub/PCMDIobs/PCMDIobs2/atmos/mon/'

pout = pin
if seperate_clims == 'y':  pout = '/p/user_pub/PCMDIobs/PCMDIobs2.0_climsOnly-beta/'
if seperate_clims == 'y':  pout = '/p/user_pub/PCMDIobs/PCMDIobs2_clims/'

lst1 = pin + '*/*/pr/latest/*.nc'
lst1 = pin + 'ERA-5/psl/gn/*/*.nc'
lst1 = pin + 'ua/ERA-5/1x1/*/*.nc'    # ERA-5 tas psl uas vas added seperately

lst_allncs = glob.glob(lst1)
lst_allncs = []

allxmls = pin + 'ua/ERA-5/1x1/v20200612/*.xml'
#allxmls = pin + 'TMP/*/1x1/*/*.xml'
lst_xmls = glob.glob(allxmls)

#use_xmls = ['ERA-5','.xml']
lst_nc = []

### TRAP ERA-5 4D XMLS but not NC files
for l in lst_allncs:
#  if 'ERA-5' not in l: 
     if l not in lst_nc: lst_nc.append(l)

print('xml list is ', lst_xmls)
for l in lst_xmls + lst_nc:   #lst_nc:   #[0:5]:
#check = 'latest' in l 
#if check is True:
 
  ldir = os.path.dirname(l) 
  realm = l.split('/')[5]
  var = l.split('/')[7]
  source = l.split('/')[8]
  ts_date = l.split('/')[10]             # yields "latest"
# ts_date_linkvalue = os.readlink(ldir)  # date of "latest" 
# print(l.split(ldir + '/'))
  fname_in = l.split(ldir + '/')[1]

  fname_in = fname_in.replace(ts_date+'_','')

  fname_out = fname_in.replace('.nc', '.' + ver + '.climo.nc')
  fname_out = fname_out.replace('.xml', '.' + ver + '.climo.nc')
# subpath = ver + '/' + var + '/' + source 
# pathout = pout + '/' + subpath 

### MKDIR AS NEEDED (SEPERATE DATABASE)
  if seperate_clims == 'y':
   subpath = realm + '/' + var + '/' + source
   pathout = pout + '/' + subpath
   mk_outdir = pout 
   for pp in subpath.split('/'):
    mk_outdir = mk_outdir + '/' + pp
    print(mk_outdir)
    try:
      os.mkdir(mk_outdir)
    except:
      pass
### MKDIR AS NEEDED (COMBINE WITH TIME SERIES)
  if seperate_clims == 'n':
   pathout = ldir + '/climo/'
   try:
    os.mkdir(pathout)
   except:
    pass

  outfd = pathout + '/' + fname_out
# print(l)
  print(outfd)
  print('---------')

#'''
  f = cdms2.open(l)
  atts = f.listglobal()

  d = f(var)  #,level=(85000.,85000.))
  d_ac =   cdutil.ANNUALCYCLE.climatology(d).astype('Float32')
  d_djf =  cdutil.DJF.climatology(d)(squeeze=1).astype('Float32')
  d_jja =  cdutil.JJA.climatology(d)(squeeze=1).astype('Float32')
  d_son =  cdutil.SON.climatology(d)(squeeze=1).astype('Float32')
  d_mam =  cdutil.MAM.climatology(d)(squeeze=1).astype('Float32')

  for v in [d_ac,d_djf,d_jja,d_son,d_mam]:
    v.id = var
    v.time_series_produced = ts_date  #ts_date_linkvalue  #ts_date

  for s in ['AC','DJF','MAM','JJA','SON']:
   if seperate_clims == 'y':  out = outfd.replace('climo',s)
   if seperate_clims == 'n':  out = outfd.replace('climo.nc',s+'.nc')
   if s == 'AC': do = d_ac
   if s == 'DJF': do = d_djf
   if s == 'MAM': do = d_mam
   if s == 'JJA': do = d_jja
   if s == 'SON': do = d_son
   do.id = var

   g = cdms2.open(out,'w+')
   g.write(do)

   for att in atts:
    setattr(g,att,f.getglobal(att))
   g.close() 
   print(do.shape,' ', d_ac.shape,' ',out)
  f.close()
#'''
