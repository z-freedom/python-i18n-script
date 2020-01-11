from idlelib.iomenu import encoding
import re
import os

print("#################################################################################")

#filepath="E:\\git\\SmartThemis\\SmartThemis_src\\webapp\\WEB-INF\\views\\vise\\freport\\webdesign\\Copy (2) of reportDesign.jsp"
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