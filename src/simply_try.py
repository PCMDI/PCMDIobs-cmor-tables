import json, ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname  = False
ctx.verify_mode     = ssl.CERT_NONE

pth = 'https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Omon.json'

res = urllib.request.urlopen(pth)
res_body = res.read()
j = json.loads(res_body.decode("utf-8"))


