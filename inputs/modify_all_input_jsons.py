import sys, os, json
import glob
from shutil import copyfile
import time

### 
# THIS CODE IS USED TO CHANGE A KEY(S) ACROSS ALL INPUT JSONS

lst = glob.glob('./*.json')

for l in lst:
## MV all FILE.json to FILE_cp.json 
   cpf = l.replace('.json','_cp.json')
   os.rename(l,cpf)
   time.sleep(0.5)

# LOAD DICTIONARY CONTENTS 
   f =  open(cpf,'r')
   d = json.load(f)
   f.close()

###########
# THIS IS THE INFO THAT GETS MODIFIED
   d['outpath'] = '/p/user_pub/PCMDIobs/'
   d['activity_id'] = 'PCMDIobs2.0-tmp'

###########
### SAVE CHANGED VALUES
   time.sleep(0.5)
   g =  open(l,'w+')
   print l,' ', d.keys()
#  json.dumps(d,g)
   json.dump(d,g,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
   g.close()


    



  
