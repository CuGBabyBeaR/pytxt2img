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
width = int(config.get('output','width'))
height = int(config.get('output','height'))
fontsize = int(config.get('output','fontsize'))
leading = int(config.get('output','leading'))
lineHeight = fontsize + leading

filename = config.get('output','name')
filetype = config.get('output','type')

font = ImageFont.truetype(fontname, fontsize)

# 读取文本
f = codecs.open(content,'r',encoding)
text = f.read()
if text[0] == u'\ufeff':
    text = text[1:]
f.close()

# 处理文本
wraptext = [u"　"]
l = fontsize
for t in text:
    fi = t
    delta = font.getsize(t)[0]
    if t == '\n':
        wraptext += [u"　"]
        l = fontsize
    elif l + delta > width:
        wraptext += [t]
        l = delta
    else:
        wraptext[-1] += t
        l += delta


# 绘制文本并保存
ltop = top
filecounter = 1
pattern = "%s%04d.%s"
filename = filename.split('.')

img = Image.open(bg)
draw = ImageDraw.Draw(img)

for i, txt in enumerate(wraptext):
    if ltop + lineHeight > height:
        img.save(pattern % (filename[0],filecounter,filename[1]), filetype)
        filecounter += 1
        img = Image.open(bg)
        draw = ImageDraw.Draw(img)
        ltop = top

    draw.text((left, ltop), txt, font=font, fill='black')
    ltop += lineHeight
    pass

# 保存到文件
img.save(pattern % (filename[0],filecounter,filename[1]), filetype)