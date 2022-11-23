import hashlib
import os
import json
import shutil
import requests

from zjyaml import *
from encryption import saveyaml as en_saveyaml
from encryption import loadyaml as en_loadyaml
path = './'

from shutil import copyfile
import update
#from server_connect import ip,ssh_port,username,password

config = loadyaml(path+'serverconfig.yaml')
print(config)
config['username']='root'  #云服务器的ssh用户名
config['password']='trz717706'  #云服务器的ssh密码
now_ver = '1.4.31'
now_info = '修复进度条不显示的bug'


e_file=['上传服务器更新.py','上传更新测试用例.py','server_connect.py']
if __name__ == '__main__':  
    path2 = './__pycache__/'    
    ##############删除编译文件夹内所有文件
    for root, dirs, files in os.walk(path2):
        for i in files:
            #if i.split('.')[-1] == 'pyc':
            os.remove(path2 + i)  
    dc=loadyaml(path+'version.yaml') 
    dc['ver']  =    now_ver
    dc['md5']={}
    dc['info']=now_info
    if 'his' not in dc.keys():
        dc['his']={}
    dc['his'][now_ver]=now_info
    #print(dc)
    
    a = []

    ############将需要编译的文件添加至列表
    for root, dirs, files in os.walk('./'):
        for i in files:
            if i.split('.')[-1] in ('yaml', 'py'):
                a.append(i)   
    import py_compile
    for i in a:
        if i.split('.')[-1]  in  ['py'] and i not in  e_file:
            print(i)
            py_compile.compile(i)

    ################################重命名编译文件，删除.cpython-37
    for root, dirs, files in os.walk(path2):

        for i in files:
            if  i.split('.')[-1]  in  ['pyc']  and i not in  e_file:
                os.rename(path2 + i, (path2 + i).replace('.cpython-310', ''))  
    ###############上传函数

    def transport_file(files):
        import paramiko
        transport = paramiko.Transport((config['server_ssh'], config['ssh_port']))
        transport.connect(username=config['username'], password=config['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        for i in files:
            sftp.put(path2 + i, '/srv/bmsreport/bms_report_/{}'.format(i)) 
        transport.close()
    #########################################复制ipt文件到编译文件夹
    

    for root, dirs, files in os.walk('./', topdown=True)   : 
        if root == './':
            fn=files
    for i in fn:
        if i.split('.')[-1] != 'py':
            copyfile(path + i, path + path2 + i) #

    ###########################计算文件MD5
    for root, dirs, files in os.walk(path+path2):
        for i in files:
            if i not in  e_file:
                dc['md5'][i] = update.GetFileMd5(path+path2 + i) 
    ######################保存版本文件和MD5到配置文件
    saveyaml(dc, path+path2 + 'version.yaml')
    saveyaml(dc, path + 'version.yaml')
    ##############将需要上传的文件添加至列表
    a = []
    for root, dirs, files in os.walk(path2):
        for i in files:
            if  i not in  e_file and  i.split('.')[-1] in ('yaml', 'pyc','xlsx'):
                a.append(i) 
    ###########上传更新文件到服务器
    print(a)
    transport_file(a)


