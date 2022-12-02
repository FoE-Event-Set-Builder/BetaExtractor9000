import re
import configparser

def run():
    config = configparser.ConfigParser()
    config.read("config.ini")
    c = config["config"]

    o = c["old"]
    n = c["new"]

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

        new = list(set(newStrings) & set(oldStrings))
        #print(len(oldStrings),len(newStrings),len(newStrings)-len(oldStrings))

    for s in new:
        if ".png" in s or ".jpg" in s: # images
            newC = newStrings[newStrings.index(s)+1]
            oldC = oldStrings[oldStrings.index(s)+1]
            if newC != oldC:
                print(oldC,"-->",newC,"|",s)
                

if __name__ == '__main__':
    run()