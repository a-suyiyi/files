import hashlib
import base64
import os
import json
import sys
os.system('python -m pip install --upgrade pip')
# os.system('pip install --upgrade requests')
import requests
if sys.argv.__len__()<2:
    exit(0)
USERNAME='a-suyiyi'
REPO='files'
TOKEN='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'
filename=sys.argv[1].split(os.sep)[-1]
api_url='https://api.github.com/repos/%s/%s/contents/%s'
def get_url(username:str, reponame:str, filename:str)->str:
    return api_url%(username,reponame,filename)
def trans_base64(data:bytes):
    return base64.b64encode(data).decode('utf-8')
'''
{
  "message": "提交说明",
  "content": "base64编码的文件内容",
  "sha": "文件的blob sha"
}
'''
def get_sha(url:str)->str:
    res=requests.get(url)
    if not res.ok:
        return ''
    d=json.loads(res.content)
    t=d.get('sha')
    return t if t is not None else ''
filedata=b''
with open(filename,'rb') as f:
    filedata=f.read()
api=get_url(USERNAME,REPO,filename)
print(api)
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
res=requests.put(api,data=json.dumps(params),headers=headers)
print(res.status_code)
