﻿import os
import shutil
import sys

def backupanddelete():
    rootdir = sys.path[0].replace('\\','/') + "/upload/all"
    parent2 = sys.path[0].replace('\\','/') + "/backup/"
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:                        
            path = os.path.join(parent,filename)
            targetDir = os.path.join(parent2,filename)
            print(targetDir)
            if '.xml' in path and "汇总" not in path:
                try:
                    shutil.copy(path,targetDir)
                except:
                    print("xls already exist!")  
            os.remove(path) #删除文件
    try:
        os.remove(sys.path[0].replace('\\','/') + "/pythonscript/png/RheoCurve.png")
    except:
        print("RheoCurve.png not exist!") 

backupanddelete()

