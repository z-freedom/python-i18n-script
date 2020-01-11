


#查找和替换普通文件中的中文
#path 文件绝对路径
#dic  字典 key-value的数据结构，key为中文，value为中文对应的英文
def findAndReplacesCnWithEn(path,dic:dict)  :
    #匹配中文
    pattern = re.compile(chanieseRegPatten)
    file = open(path, encoding=commonencoding,mode="r+")
    strfile = file.read()
    # 查找文件所有中文
    CNList = pattern.findall(strfile)

    for chinese in CNList:
        if chinese in dic.keys():
            replpatten = "(?<=[^\u4e00-\u9fa5])" + chinese + "(?=[^\u4e00-\u9fa5])"
            result = re.sub(replpatten,dic.get(chinese), strfile)
    file.close()
    return result