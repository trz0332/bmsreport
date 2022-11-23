
import hashlib
import os
import json
import shutil
import requests
try:
    from .zjyaml import *
    from .encryption import saveyaml as en_saveyaml
    from .encryption import loadyaml as en_loadyaml
    path = './ipt/'
except:
    from zjyaml import *
    from encryption import saveyaml as en_saveyaml
    from encryption import loadyaml as en_loadyaml
    path = './'

from shutil import copyfile
config = loadyaml(path + 'serverconfig.yaml')
local_info = loadyaml(path + 'version.yaml')

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def get_version():
    try:
        info = requests.get(config['server_']+':'+str(config['api_port'])+'/weixin/api/v1.0/bmsreportappvison', timeout=1)
        print(info)
        if info.status_code == 200:
            info = info.json()
            return info
        else:
            return False
    except:
        return False


def compare(a, b):
    la = a.split('.')   
    lb = b.split('.')
    f = 0
    if len(la) > len(lb):
        f = len(la)
    else:
        f = len(lb)
    for i in range(f):
        try:
            if int(la[i]) > int(lb[i]):
                return('>')
                
            elif int(la[i]) == int(lb[i]):
                continue
            else:
                return('<')   
        except IndexError as e:
            if len(la) > len(lb):
                return('>')
                
            else:
                return('<')
    return('=')



def download_file(ver, filename):
    url=config['server_']+':'+str(config['api_port'])
    down_url= '/download/{}/'.format(filename)
    t = requests.get(url=url+down_url,stream=True,timeout=1)
    if t.status_code==200:
        with open(path+ver+'/'+filename,'wb') as f:
            t.raw.decode_content=True
            shutil.copyfileobj(t.raw,f)
        return True
    else:
        return False



def bj_ver():
    server_info = get_version()
    if server_info:
        sa = compare(local_info['ver'], server_info['ver'])
        return (sa, server_info,local_info)
    else:
        return '//',local_info,local_info



def _update(server_info):
    file_list=[]
    local_info=loadyaml(path+'version.yaml')
    directory = os.getcwd()
    if not os.path.exists(path+server_info['ver']+'/'):
        os.mkdir(directory+path[1:]+server_info['ver']+'/')
    for i in  server_info['md5'].keys():
        if i not in local_info['md5'].keys():
            if   download_file(server_info['ver'],i):
                file_list.append(i)
            else :
                return False,i
        else:
            if    server_info['md5'][i] != local_info['md5'][i]:
                if  download_file(server_info['ver'],i):        
                    file_list.append(i)
                else:
                    return False,i
    for i in ['version.yaml','config.yaml']:
        if   download_file(server_info['ver'],i):
            file_list.append(i)
        else :
            return False,i
        
    return file_list,server_info['ver']

        
def upgru(file_list,path1):
    try:
        if 'update.pyc' in file_list:
            os.remove(path+'update.pyc')
            copyfile(path+path1+'/'+'update.pyc',path+'update.pyc')

        for i in file_list:
            if os.path.exists(path+i):
                os.remove(path+i)
            copyfile(path+path1+'/'+i,path+i)
        return True
    except Exception as err:
        print(err)
        return False


if __name__=='__main__':
    print(get_version())