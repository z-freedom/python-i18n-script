from idlelib.iomenu import encoding
import re
import os

print("#################################################################################")

#filepath="your jsp file path"
listfile="E:\\new.txt"
print(listfile)

file_object = open(listfile,encoding="utf-8")

while 1:
    filepath = file_object.readline().strip()
    if filepath.startswith("#"):
        continue
    else:
        pattern =re.compile(u"[\u4e00-\u9fa5]+")
        print(filepath)
        file = open(filepath,encoding="utf-8")
        try: 
            for line in file:
                   gr=re.findall(pattern, line)
                   if len(gr) != 0:
                        print(gr)
        finally:
            file.close()
