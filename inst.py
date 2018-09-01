
from PyInstaller.__main__ import run
# -F:打包成一个EXE文件
# -w:不带console输出控制台，window窗体格式
# --paths：依赖包路径
# --icon：图标
# --noupx：不用upx压缩
# --clean：清理掉临时文件
from PyQt5 import sip
import sys, os
import save_ico
 
if __name__ == '__main__':
    opts = [ '-w','-F','--icon=save.ico','--icon=timg.jpg', '--noupx', '--clean',
            'ui.py','--hidden-import=queue']
    run(opts)