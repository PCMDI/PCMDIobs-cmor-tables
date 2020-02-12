import os, glob

# THIS SCRIPT USES CDSCAN TO PRODUCE XMLS IN PCMDIobs IN CASES WHERE A TIME SERIES SPANS MULTIPLE netCDF FILES


pin = '/p/user_pub/PCMDIobs/PCMDIobs2.0-beta/atmos/'


xmls_needed =  ['*/*/ERA-5/*/*/']

for x in xmls_needed:
  pth = pin + x
 
  lst = glob.glob(pth)

  for l in lst:
   pthi = os.path.dirname(l)
   print(pthi)

   var = pthi.split('/')[7]
   source = pthi.split('/')[8]

   os.chdir(pthi)

   os.popen('cdscan -x ' + var + '_' + source + '.xml *.nc').readlines()




 
