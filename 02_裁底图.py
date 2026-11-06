# -*- coding: utf-8 -*-
from PIL import Image
import shutil, os

RAW = r'C:\Users\ASUS\AppData\Local\Doubao\User Data\ClipboardTemp\8eb529f1-4a80-45bd-a6cd-708725028e71.png'
DIR = r'C:\Users\ASUS\Desktop\今天\3D校园'
OUT = os.path.join(DIR, '底图.png')

shutil.copy(RAW, os.path.join(DIR, '底图_raw.png'))
im = Image.open(RAW)
print('原始尺寸:', im.size)

# 裁掉顶部菜单栏(~110px)、左侧收藏面板(~280px)、底部状态栏(~108px)
# 地图区域: left=282, top=112, right=1870, bottom=985
crop = im.crop((282, 112, 1870, 985))
crop.save(OUT)
print('裁后尺寸:', crop.size, '->', OUT)
