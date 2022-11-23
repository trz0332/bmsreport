
import base64,time,re
import binascii
import yaml
# 秘钥
KEY='mHAxsLYz'
KEY='717706Tt'
CUSTOM_ALPHABET = b'6jKB+GDsJvmdXqPkeHTF4nMY2af97QcZtLRohO/b1ECVgIy3ANi5zxpWlrwSu8U0'
STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

ENCODE_TRANS = bytes.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
DECODE_TRANS = bytes.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)


def zdy_encode(input,model=0):
    if model==0:
        return base64.b64encode(input).translate(ENCODE_TRANS)
    else:
        return base64.b64encode(input)

def zdy_decode(input,model=0):
    if model==0:
        return base64.b64decode(input.translate(DECODE_TRANS))
    else:
        return base64.b64decode(input)

def loadyaml(filename,model=0):
    #path=''
    try:
        with open(filename,'r',encoding='UTF-8') as f :
            zal=f.read()
            zal=zdy_decode(zal.encode(),model).decode('utf-8')
            config=yaml.load(zal,Loader=yaml.FullLoader)
            #print(config)
    except BaseException as err:
        print(err,2)
        return False
    else:
        return config
def saveyaml(data,filename,model=0):    #保存配置
    with open(filename, 'w+',encoding='UTF-8') as stream:
        try:
            zal=str(data)
            zal=zdy_encode(zal.encode(),model).decode('utf-8')
            stream.write(zal)
        except Exception as e :
            return False
        else:return True

def base64_2img(base64_data,img_filename,model=0):    #base64.b64decode(data)
    imgdata = zdy_decode(base64_data,model)
    with open(img_filename,'wb') as file:
        file.write(imgdata)


 

if  __name__=='__main__':
    #sa=zdy_encode('oHw-X1SDN2cbxb_Vo0p6ZwWQ4WbQ'.encode())
    #print(sa)
    #sb=zdy_decode(sa)
    #print(sb)
    #sa=des_encrypt(STANDARD_ALPHABET)
    #print(shuffle_str(sa))
    #saveyaml({'a':12},'test.yaml')
    #print(loadyaml('test.yaml'))
    config = loadyaml('config.yaml')


