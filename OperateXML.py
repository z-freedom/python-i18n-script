from idlelib.iomenu import encoding
import re


filepath= input('请输入文件路径：')
file = open(filepath,encoding="utf-8") 
str1=file.readlines()
print(str1)
#pattern =re.compile("<bean.+</bean>") 
#gr=re.findall(pattern, str)
#print(gr)
file.close()