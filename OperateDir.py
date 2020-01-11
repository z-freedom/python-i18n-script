from idlelib.iomenu import encoding
import re
import os
from builtins import UnicodeDecodeError
#迭代目录
def findAndPrintAllFilesByDir(rootDir):
    listfilespath=[]
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path): 
            Test2(path) 
        else :
            print("############################################找到文件，开始查找文件中的中文#####################################文件编号：",i)
            print(path)
            file_object = open(path,encoding="utf-8")
            try: 
                pattern =re.compile(u"[\u4e00-\u9fa5]+")
                for line in file_object:
                    gr=re.findall(pattern, line)
                    if len(gr) != 0:
                        print(gr)
                        listfilespath.append(gr)
                        print()
            except  UnicodeDecodeError:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!抛出异常!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                continue
            file_object.close()
    return listfilespath
rootDir=input("请输入要迭代的目录：")
Test2(rootDir)