import re
import configparser
import requests
from natsort import natsorted

def run():
    config = configparser.ConfigParser()
    config.read("config.ini")
    c = config["config"]

    o = c["old"]
    n = c["new"]
    filter = c["filter"]
    

    with open(o) as f:
        oldText = f.read()

    with open(n) as f:
        newText = f.read()

    if True:
        newText = newText.replace(r'"\\"','')
        newText = newText.replace(r'\"','')
        newText = newText.replace('\'\"\'','\'\'')
        newText = newText.replace('\"\'\"','\"\"')
        newText = newText.replace('=\'\"','=\"')
        newText = newText.replace('\'\"','\'')
        newText = newText.replace('\"\'#','\'#')
        newText = newText.replace('\"\' +','\' +')
        newText = newText.replace('Expected \"\'','Expected \'')
        newText = newText.replace('=\"\'','=\'')
        newText = newText.replace('\"1em \'','\'1em \'')
        newText = newText.replace('\"\' is','\' is')
        newText = newText.replace('\"Profile must be of type','Profile must be of type')

        oldText = oldText.replace(r'"\\"','')
        oldText = oldText.replace(r'\"','')
        oldText = oldText.replace('\'\"\'','\'\'')
        oldText = oldText.replace('\"\'\"','\"\"')
        oldText = oldText.replace('=\'\"','=\"')
        oldText = oldText.replace('\'\"','\'')
        oldText = oldText.replace('\"\'#','\'#')
        oldText = oldText.replace('\"\' +','\' +')
        oldText = oldText.replace('Expected \"\'','Expected \'')
        oldText = oldText.replace('=\"\'','=\'')
        oldText = oldText.replace('\"1em \'','\'1em \'')
        oldText = oldText.replace('\"\' is','\' is')
        oldText = oldText.replace('\"Profile must be of type','Profile must be of type')


        oldStrings = re.findall('"([^"]*)"', oldText)
        newStrings = re.findall('"([^"]*)"', newText)

        new = list(set(newStrings) - set(oldStrings))
        #print(len(oldStrings),len(newStrings),len(newStrings)-len(oldStrings))

    excluded = []
    xmls = []
    images = []
    info = []
    other = []
    for id in range(len(new)):
        s = new[id]
        try: # checksums
            int(s, 16)
            excluded.append(s)
        except:
            if ".png" in s: # images
                if filter.upper() not in s.upper():
                    continue
                nId = newStrings.index(s)
                images.append(s.replace(".png","")+"-"+str(newStrings[nId+1])+".png")
            elif ".jpg" in s: # images
                if filter.upper() not in s.upper():
                    continue
                nId = newStrings.index(s)
                images.append(s.replace(".jpg","")+"-"+str(newStrings[nId+1])+".jpg")
            elif ".xml" in s: # xml files
                xmls.append(s)
            elif "|" in s: # Information texts (they're usually of the form "[event]|[information]")
                info.append(s)
            else: # Everything else
                other.append(s)
    
    images = natsorted(images)
    xmls = natsorted(xmls)
    info = natsorted(info)
    other = natsorted(other)

    if c.getboolean("other"):
        if len(other) == 0:
            print("\nNo other new strings")
        else:
            print("\nOther new strings:")
        for i in other:
            print(i)
            
    if c.getboolean("xml"):
        if len(xmls) == 0:
            print("\nNo new xml files")
        else:
            print("\nNew xml files:")
        for x in xmls:
            link = "https://foezz.innogamescdn.com/assets" + x
            link = link.replace("assets/assets","assets")
            print(link)
            
    if c.getboolean("info_texts"):
        if len(info) == 0:
            print("\nNo new information texts")
        else:
            print("\nNew information texts:")
        for i in info:
            print(i)

    if c.getboolean("image_bb"):
        if len(images) > 0:    
            print("\nBB Format:")
        for img in images:
            link = "https://foezz.innogamescdn.com/assets" + img
            link = link.replace("assets/assets","assets")
            print("[img]" + link + "[/img]")
            print(link.split("/")[-1].replace("https://foezz.innogamescdn.com/assets/",""))
            print()

    if c.getboolean("image_links"):
        if len(images) == 0:
            print("\nNo new images :(")
        else:
            print("\nNew images:")
        for img in images:
            link = "https://foezz.innogamescdn.com/assets" + img
            link = link.replace("assets/assets","assets")
            print(link) 

    print(f"Found {len(images)} new images, {len(xmls)} new xml files, {len(info)} new info texts, and {len(other)} other new strings")

    if c.getboolean("downloadNew"):
        if len(images) != 0:
            print("Downloading images...")
            for img in images:
                try:
                    link = "https://foezz.innogamescdn.com/assets" + img
                    link = link.replace("assets/assets","assets")
                    path = str(c["folderNew"]) + "\\" + img.replace("/","_")
                    img_data = requests.get(link).content
                    with open(path,"wb") as h:
                        h.write(img_data)
                except:
                    if i == 4:
                        print("Failed to grab:",img)
            print("Download finished")

if __name__ == '__main__':
    run()