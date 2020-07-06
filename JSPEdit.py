from idlelib.iomenu import encoding
import re
import os
import sys
from builtins import UnicodeDecodeError

#配置类
class Conf(object):
    #文件编码
    fileEncoding="UTF-8"
    #中文正则表达式
    chineseReg=u"[\u4e00-\u9fa5]+"
    #注释正则表达式
    jspCommentReg="<!--(\s|.)*?-->|\/\*(\s|.)*?\*\/|<%--(\s|.)*?--%>"
    #标准字典路径
    standardDictPath=".\\file\\stdDic.cfg"
    #生成中文配置文件路径
    CNProfPath=".\\result\\CN.properties"
    # 生成英文配置文件路径
    ENProfPath=".\\result\\EN.properties"
    #JSP文件和前缀保存文件路径
    jspPathAndPrefSaveFilePath=".\\file\\jspPathAndPref.cfg"
    specStr=r"¥#####$###@"
    #项目所在的根目录
    rootDir=r"your dir"
    #debug输出所有处理结果，输出提示信息
    loglevel="dubug"
    def __init__(self):
        super.__init__()

#查找和替换JSP中文，忽略注释
#proppertiesDic 字典Key为配置参数名称，value为英文翻译
def findAndReplacesCnWithEnOfJSP(jspPath,proppertiesDic:dict)  :
    #匹配中文
    pattern = re.compile(Conf.chineseReg)
    #匹配注释
    ignorePatten=re.compile(Conf.jspCommentReg)
    file = open(jspPath, encoding=Conf.fileEncoding, mode="r+")
    str1='<%=new String(bundle.getString("'
    str2='").getBytes("ISO-8859-1"), "UTF8")%>'
    if os.path.splitext(jspPath)[1]==".jsp":
        strfile=file.read()
        #先保存注释<!-- 注释内容> -->或/* 注释内容  */ 或<%--  注释内容 --%>到列表
        commentsList=ignorePatten.findall(strfile)
        print("发现注释：",list(commentsList))
        #然后把注释特殊处理，用文件中不存在的字符串代替，方便一会儿替换回来
        result=re.sub(ignorePatten,Conf.specStr,strfile)
        #找到所有中文，此时已经忽略注释
        toBeReplaceOfCnList=pattern.findall(result)
        print("即将被替换的中文：",list(toBeReplaceOfCnList))
        #替换
        for chinese in toBeReplaceOfCnList:
            if chinese in proppertiesDic.values():
                #根据value找key,也即参数名
                paramname=list(proppertiesDic.keys())[list(proppertiesDic.values()).index(chinese)]
                #前瞻后视，精准匹配中文
                replPatten="(?<=[^\u4e00-\u9fa5])"+chinese+"(?=[^\u4e00-\u9fa5])"
                result=re.sub(replPatten,str1+paramname+str2,result)
        #把注释在替换回来
        for comment in commentsList:
            result,count=re.subn(Conf.specStr,comment,result,count=1)
        if Conf.loglevel == "dubug":
            print(result)
    else:
        print("警告！该文件不是JSP文件，程序将跳过此文件",file=sys.stderr)
    file.seek(0)
    file.truncate()
    file.write(result)
    file.close()
    return

#读取JSP文件中的中文，忽略注释
def findChineseCharacterFromJspFileIgnoreComment(jspPath)  :
    #匹配中文
    pattern = re.compile(Conf.chineseReg)
    result=[]
    #匹配文件中的注释包括单行注释和块注释
    commentPatten=re.compile(Conf.jspCommentReg)
    file = open(jspPath, encoding=Conf.fileEncoding)
    strfile=file.read()
    #删除代码里面的注释
    strfile=re.sub(commentPatten,"",strfile)
    result=pattern.findall(strfile)
    #print(result)
    file.close()
    return  result

#读取中英文标准翻译
#返回字典 key为中文，value为英文
#参数 字典txt文件路径和中英文分隔符
def getStdDic(stdDicPath=Conf.standardDictPath) ->dict:
    stdDicFile=open(Conf.standardDictPath,encoding=Conf.fileEncoding)
    resultDic={}
    for line in stdDicFile:
        rel=line.split("=")
        rel[1]=rel[1].strip()
        resultDic[rel[0]]=rel[1]
    #print(resultDic)
    return  resultDic

#生成配置文件
#JSPPath JSP文件路径，JSPPref参数公共前缀,lang中文请输入CN，英文请输入EN
def propertiesFile(JSPPath,JSPPref) ->dict:
    cnlist = findChineseCharacterFromJspFileIgnoreComment(JSPPath)
    stdDic = getStdDic()
    CNreldic={}
    ENreldic={}
    baseProppertiesDic = {"CNreldic":CNreldic,"ENreldic":ENreldic}
    CN_file = open(Conf.CNProfPath, encoding="utf-8", mode="a+")
    EN_file = open(Conf.ENProfPath, encoding="utf-8", mode="a+")
    #生成中文配置文件
    if 1:
        JSPName=JSPPath.replace(Conf.rootDir, "")+os.path.basename(JSPPath)
        CN_file.write("\n"+"#"+JSPName+"\n")
        for item in cnlist:
            if item in stdDic.keys():
                key=JSPPref + "." + stdDic.get(item).replace(" ", "")
                #去重
                if key not in CNreldic.keys():
                    line=key +"="+item
                    if Conf.loglevel=="dubug":
                        print(line)
                    CNreldic[key]=item
                    CN_file.write(line)
                    CN_file.write("\n")
                else:
                    if Conf.loglevel == "dubug":
                        print("重复的key:",key, "=", item)
    #print("---------------------------")
    # 生成英文配置文件
    if 1:
        JSPName = JSPPath.replace(Conf.rootDir, "") + os.path.basename(JSPPath)
        EN_file.write("\n"+"#"+JSPName+"\n")
        for item in cnlist:
            if item in stdDic.keys():
                key = JSPPref + "." + stdDic.get(item).replace(" ", "")
                # 去重
                if key not in ENreldic.keys():
                    line = key+ "="+ stdDic.get(item)
                    if Conf.loglevel=="dubug":
                        print(line)
                    ENreldic[key] = stdDic.get(item)
                    EN_file.write(line)
                    EN_file.write("\n")
                else:
                    if Conf.loglevel == "dubug":
                        print("重复的key:", key, "=", item)
    CN_file.close()
    EN_file.close()
    return baseProppertiesDic
#从jspPathAndPref.cfg获取所有需要修改JSP文件路径以及参数公共后缀
def getPrefAndJSPPathFromFile() ->dict:
    file=open(Conf.jspPathAndPrefSaveFilePath,encoding=Conf.fileEncoding)
    PrefAndJSPPathDic={}
    for line in file:
        list=line.split("=")
        if len(list) !=2:
            print("---------------------请检查文件%s内容是否符合规范-------------------"%Conf.jspPathAndPrefSaveFilePath)
            exit("请检查文件内容是否符合规范")
        else:
            PrefAndJSPPathDic[list[0]]=list[1].replace("\n","")
    if Conf.loglevel=="dubug":
        for key in PrefAndJSPPathDic:
            print(key,"=",PrefAndJSPPathDic.get(key))
    return  PrefAndJSPPathDic
#如果已经包涵，将跳过该文件
def addi18n(path):
    pat1=re.compile("""(<%@ include file="/form.jsp"%>)""")
    str=""""<%@ include file="/i18n.jsp" %>"""
    pat2 = re.compile(str)
    jspfile=open(path,mode="r+",encoding="utf-8")
    strfile=jspfile.read()
    if len(pat2.findall(strfile))!=0:
        print("该JSP文件已经包含",str)
        print(path)
    else:
        strfile,n=pat1.subn('<%@ include file="/form.jsp"%>\n<%@ include file="/i18n.jsp" %>',strfile)
        print("增加%s的次数为："%str,n)
        print(path)
        jspfile.seek(0)
        jspfile.truncate()
        jspfile.write(strfile)
    rel=pat1.findall(strfile)
    jspfile.close()
    #print(rel)

def main():
    #从jspPathAndPref.cfg中获取所有需要修改JSP文件路径以及参数公共后缀
    print("开始读取jspPathAndPref.cfg文件，获取所有要修改的文件以及对应的前缀")
    listFilePathAndPref=getPrefAndJSPPathFromFile()
    for pref in listFilePathAndPref:
        path = listFilePathAndPref.get(pref)
        print("开始处理JSP文件，文件名称:", path)
        print("开始生成中英文配置文件............")
        CNreldic = propertiesFile(path, pref).get("CNreldic")
        print("开始查找替换jsp文件里面的中文............")
        findAndReplacesCnWithEnOfJSP(path, CNreldic)
        print(r'开始增加<%@ include file="/form.jsp"%>')
        addi18n(path)
        print("该文件处理完毕！\n\n")


main()
