from idlelib.iomenu import encoding
import re
import os

print("#################################################################################")

#filepath="file path"
filepath= input('请输入文件路径：')

pattern =re.compile(u"[\u4e00-\u9fa5]+") 
file = open(filepath,encoding="utf-8")
try: 
    for line in file:
        gr=re.findall(pattern, line)
        if len(gr) != 0:
            print(gr)
finally:
    file.close()
