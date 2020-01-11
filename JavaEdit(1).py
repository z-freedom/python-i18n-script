


#查找Java文件中的中文，忽略注释
#path 文件绝对路径
#返回中文列表
def findCnFromJavaFileIgnoreComment(path)  :
    #匹配中文
    pattern = re.compile(chanieseRegPatten)
    #存放返回结果
    result=[]
    #匹配文件中的注释包括单行注释和块注释
    ignorePatten=re.compile("/\*{1,2}[\s\S]*?\*/|//[\s\S]*?\n")
    file = open(path, encoding=commonencoding)
    strfile=file.read()
    #删除Java代码里面的注释
    strfile=re.sub(ignorePatten,"",strfile)
    #查找中文
    result = pattern.findall(strfile)
    file.close()
    return  result

#查找和替换Java中文，忽略注释
def findAndReplacesReplacesCnWithEnOfJava(path,dic:dict)  :
    #匹配中文
    pattern = re.compile(chanieseRegPatten)
    #匹配注释
    ignorePatten=re.compile("/\*{1,2}[\s\S]*?\*/|//[\s\S]*?\n")
    file = open(path, encoding=commonencoding, mode="r+")
    strfile=file.read()
    #先保存注释到列表中
    comments=ignorePatten.findall(strfile)
    #然后把注释特殊处理，用文件中不存在的字符串代替，方便一会儿替换回来
    result=re.sub(ignorePatten,"#############",strfile)
    #找到所有中文，此时以及忽略注释
    toBeReplaceList=pattern.findall(result)
    #替换
    for word in toBeReplaceList:
        if word in dic.keys():
            result=result.replace(word,dic.get(word))
    #print(result)
    #把注释在替换回来
    for comment in comments:
        result=result.replace("#############",comment,1)
    print(result)
    file.write(result)
    return