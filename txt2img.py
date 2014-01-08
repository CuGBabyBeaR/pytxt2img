import codecs, ConfigParser 
from PIL import Image,ImageDraw,ImageFont

def main():
    # read configuration
    print 'read configuration'
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

    # read content
    print 'read content'
    f = codecs.open(content,'r',encoding)
    text = f.read()
    if text[0] == u'\ufeff':
        text = text[1:]
    f.close()

    # text process
    print 'text process'
    wraptext = [u"\u3000"]
    l = fontsize
    for t in text:
        fi = t
        delta = font.getsize(t)[0]
        if t == '\n':
            wraptext += [u"\u3000"]
            l = fontsize
        elif l + delta > width:
            wraptext += [t]
            l = delta
        else:
            wraptext[-1] += t
            l += delta


    # draw text and save
    ltop = top
    filecounter = 1
    pattern = "%s%04d.%s"
    filename = filename.split('.')

    img = Image.open(bg)
    draw = ImageDraw.Draw(img)

    for i, txt in enumerate(wraptext):
        if ltop + lineHeight > height:
            name = pattern % (filename[0],filecounter,filename[1])
            print 'saving \"%s\" ...' % name
            img.save(name, filetype)
            filecounter += 1
            img = Image.open(bg)
            draw = ImageDraw.Draw(img)
            ltop = top

        draw.text((left, ltop), txt, font=font, fill='black')
        ltop += lineHeight
        pass

    name = pattern % (filename[0],filecounter,filename[1])
    print 'saving \"%s\" ...' % name
    img.save(name, filetype)
    pass

if __name__ == '__main__':
    main()
