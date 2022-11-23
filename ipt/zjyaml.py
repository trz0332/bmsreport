import yaml
def loadyaml(filename):
    #path=''
    try:
        with open(filename,'r',encoding='UTF-8') as f :
            config=yaml.load(f,Loader=yaml.FullLoader)
    except BaseException as err:return err
    else:return config
def saveyaml(data,filename):    #保存配置
    with open(filename, 'w+',encoding='UTF-8') as stream:
        try:
            yaml.dump(data, stream,default_flow_style=False,encoding='utf8',allow_unicode=True)
        except Exception as e :
            print(e)
            return False
        else:return True