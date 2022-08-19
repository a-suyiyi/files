import hashlib
import base64
import os
import json
import sys
import requests
if len(sys.argv)<2:
    exit(0)
USERNAME='a-suyiyi'
REPO='files'
TOKEN=bytes([103,104,112,95,103,110,100,52,54,97,56,71,99,80,109,120,54,89,97,85,55,120,67,109,83,87,87,89,72,104,88,81,105,89,48,83,118,102,109,102]).decode('utf-8')
filename=sys.argv[1].split(os.sep)[-1]
api_url='https://api.github.com/repos/%s/%s/contents/%s'
def get_url(username:str, reponame:str, filename:str)->str:
    return api_url%(username,reponame,filename)
def trans_base64(data:bytes):
    return base64.b64encode(data).decode('utf-8')
def get_sha(url:str)->str:
    res=requests.get(url)
    if not res.ok:
        return ''
    d=json.loads(res.content)
    t=d.get('sha')
    return t if t is not None else ''
print('reading file...')
filedata=b''
with open(filename,'rb') as f:
    filedata=f.read()
api=get_url(USERNAME,REPO,filename)
print('getting blob sha')
sha=get_sha(api)
headers={
    "Accept":"application/vnd.github+json",
    "Authorization":(f"token %s"%(TOKEN))
}
params={
    "message":sys.argv[1],
    "content":trans_base64(filedata),
    "commiter":{
        "name":USERNAME,
        "email":"hbxxsylbeifen1@126.com"
    }
}
if sha:
    params["sha"]=sha
print('creating/updating file')
res=requests.put(api,data=json.dumps(params),headers=headers)
print("success" if res.ok else "failed")
