# signature calculation from the api sample at
# https://developer.ecoflow.com/us/document
# NOTE: this is a testing program, ecoflow.py has some real (bug ugly) code
import requests
import hmac
import hashlib

accessKey="Fp4SvIprYSDPXtYJidEtUAd1o"
secretKey="WIbFEKre0s6sLnh4ei7SPUeYnptHG6V"
nonce=345164
timestamp=1671171709428
params = "params.cmdSet=11&params.eps=0&params.id=24&sn=123456789"
oksig = "07c13b65e037faf3b153d51613638fa80003c4c38d2407379a7f52851af1473e"
okkvstring = "params.cmdSet=11&params.eps=0&params.id=24&sn=123456789&accessKey=Fp4SvIprYSDPXtYJidEtUAd1o&nonce=345164&timestamp=1671171709428"

url = f"{params}&accessKey={accessKey}&nonce={nonce}&timestamp={timestamp}"
print(url)
if url != okkvstring:
    print("URL invalid!")
signature = hmac.new(bytes(secretKey, 'latin-1'), msg=bytes(url, 'latin-1'), digestmod=hashlib.sha256).hexdigest()
print(signature)
if oksig != signature:
    print("sig invalid!")
