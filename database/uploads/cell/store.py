import os
import shutil
import sys

def backupanddelete():
    rootdir = sys.path[0].replace('\\','/') + "/uploads"
    parent2 = sys.path[0].replace('\\','/') + "/backups/"
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:                        
            path = os.path.join(parent,filename)
            targetDir = os.path.join(parent2,filename)
            #print(targetDir)
            if '.xls' or '.xlsx' in path:
                try:
                    shutil.copy(path,targetDir)
                except:
                    print("Document already exist!")  
            os.remove(path) #删除文件

backupanddelete()

