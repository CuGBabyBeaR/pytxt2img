# -*- coding: utf-8 -*-
import codecs, ConfigParser 
from PIL import Image,ImageDraw,ImageFont

# 读取配置
config = ConfigParser.ConfigParser()
config.read('config.cfg')

bg = config.get('input','background')
content = config.get('input','content')
encoding = config.get('input','encoding')
fontname = config.get('input','fontname')

left = int(config.get('output','left'))
top = int(config.get('output','top'))
lineWidth = int(config.get('output','lineWidth'))
fontsize = int(config.get('output','fontsize'))
leading = int(config.get('output','leading'))
lineHeight = fontsize + leading

filename = config.get('output','name')
filetype = config.get('output','type')

img = Image.open(bg)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(fontname, fontsize)

# 读取文本
f = codecs.open(content,'r',encoding)
text = f.read()
if text[0] == u'\ufeff':
    text = text[1:]
f.close()

# 绘入文本
wraptext = [u"　"]
l = 0
for t in text:
    fi = t
    delta = font.getsize(t)[0]
    if t == '\n':
        wraptext += [u"　"]
        l = 0
    elif l + delta > lineWidth:
        wraptext += [t]
        l = delta
    else:
        wraptext[-1] += t
        l += delta

for i, txt in enumerate(wraptext):
    draw.text((left, lineHeight * i + top), txt, font=font, fill='black')
    pass

# 保存到文件
img.save(filename, filetype)