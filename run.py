import scripts.download
import scripts.compare
import scripts.compare_img
import scripts.checksum_diff
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
c = config["config"]
print("==========================================================")

if c.getboolean("compareStrings"):
    print("=== Comparing Strings ===")
    scripts.compare.run()
    print("==========================================================")

if c.getboolean("download"):
    print("=== Downloading Images ===")
    print("This might take a while depending on your internet speeds.")
    print("The last few files usually takes considerably more time.")
    scripts.download.run()
    print("==========================================================")
    
if c.getboolean("compareImages"):
    print("=== Comparing Images ===")
    scripts.compare_img.run()
    print("==========================================================")

if c.getboolean("compareChecksums"):
    print("=== Comparing Checksums ===")
    scripts.checksum_diff.run()
    print("==========================================================")

