from os import listdir
from os.path import isfile, join
import cv2
import numpy as np
import configparser

def run():
    config = configparser.ConfigParser()
    config.read("config.ini")
    c = config["config"]
    
    files = [c["old"],c["new"]]
    folders = [f.strip(".txt") for f in files]

    newPath = folders[1]
    oldPath = folders[0]

    new = [f for f in listdir(newPath) if ".png" in f or ".jpg" in f]
    old = [f for f in listdir(oldPath) if ".png" in f or ".jpg" in f]
    onlyNew = [f for f in new if f not in old]
    onlyOld = [f for f in old if f not in new]
    common = [f for f in new if f in old]
    if len(onlyNew) > 0:
        print("\nImages only found in new:")
        for f in onlyNew:
            print(f.replace("_","/"))
    if len(onlyOld) > 0:
        print("\nImages only found in old:")
        for f in onlyOld:
            print(f.replace("_","/"))

    print("\nChecking for differences... (ignore the 'libpng' warnings)")
    errors = 0
    for f in common:
        n = cv2.imread(newPath+"\\"+f)
        o = cv2.imread(oldPath+"\\"+f)

        try:
            if n.shape == n.shape:
                pass
        except Exception:
            errors += 1
            print("Error with new image:",f)
            continue
        
        try:

            if o.shape == o.shape:
                pass
        except Exception:
            errors += 1
            print("Error with old image:",f)
            continue
        
        
        if n.shape != o.shape:
            print("-> New image size:",f.replace("_","/"))
            if c.getboolean("downloadDiff"):
                cv2.imwrite(str(c["folderDiff"])+"\\"+f+"_New.png",n)
                cv2.imwrite(str(c["folderDiff"])+"\\"+f+"_Old.png",o)
        
        else:
            dif = cv2.subtract(n,o)
            res = not np.any(dif)
            if not res:
                print("-> Difference found in:",f.replace("_","/"))
                if c.getboolean("downloadDiff"):
                    cv2.imwrite(str(c["folderDiff"])+"\\"+f+"_New.png",n)
                    cv2.imwrite(str(c["folderDiff"])+"\\"+f+"_Old.png",o)
                    cv2.imwrite(str(c["folderDiff"])+"\\"+f+"_Dif.png",dif)
    print(errors,"image errors")
                
if __name__ == '__main__':
    run()