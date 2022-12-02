import requests
import re
import threading
import time
import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")
c = config["config"]

files = [c["old"],c["new"]]
folders = [f.strip(".txt") for f in files]
servers = [c["old_server"],c["new_server"]]
exclude_file = c["exclude_file"]
runScript = config.getboolean("config","download")

def download(png,folder,server):
    for i in range(5):
        try:
            if ".png" in png[0]:
                img = "https://foe" + server + ".innogamescdn.com/assets" + png[0].replace(".png","-"+str(png[1])+".png")
            else:
                img = "https://foe" + server + ".innogamescdn.com/assets" + png[0].replace(".jpg","-"+str(png[1])+".jpg")
            img.replace("assets/assets","assets")
            path = folder + "\\" + png[0].replace("/","_")
            img_data = requests.get(img).content
            with open(path,"wb") as h:
                h.write(img_data)
            break
        except:
            if i == 4:
                print("Failed to grab:",png)
                #traceback.print_exc()
    return

def run():
    if not runScript:
        return
    for ix in range(2):
        if os.path.isdir(folders[ix]):
            print(f"\nFolder for \"{files[ix]}\" found, delete folder to (re)download files")
            continue
        else:
            os.mkdir(folders[ix])
            
        
        n = files[ix]

        with open(n) as f:
            newTexts = f.read()

        splits = newTexts.split(".baseUrl,{")
        newText = splits[1].split("\"/sounds/tavern/tavernsounds.ogg\"")[0]

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

            newStrings = re.findall('"([^"]*)"', newText)

            new = [item for item in newStrings]

            pngs = {}

            for id in range(len(new)):
                s = new[id]
                try: 
                    if ".png" in s or ".jpg" in s:
                        if s == ".png" or s == ".jpg":
                            continue         
                        pngs[s] = new[id+1]
                except:
                    continue

        print(f"Number of images found in \"{files[ix]}\": {len(pngs)}")
        
        excluded = []

        with open(exclude_file,"r") as f:
            excluded = f.read().splitlines()

        
        download_img = [[p,c] for p,c in pngs.items() if p not in excluded]
        images = len(download_img)
        
        print("Downloading",images,"images,",len(pngs)-images,"excluded")

        start = time.time()
        t = []
        i = 0
        path = folders[ix]
        server = servers[ix]
        while True:
            while len(t) <= 500 and i < images:
                t.append(threading.Thread(target=download,args=[download_img[i],path,server]))
                t[-1].daemon = True
                t[-1].start()
                i += 1
            
            if len(t) == 0:
                break

            length = len(t)
            for th in range(length):
                inv = length-th-1
                if not t[inv].is_alive():
                    del t[inv]
            print("Downloaded: " + str(i-len(t)) + "/" + str(images) + " (Elapsed Time: " + str(round(time.time()-start,2))+")",end="\r")
            time.sleep(0.1)
    print("Download Completed - ")
if __name__ == '__main__':
    run()