import os
import numpy as np
os.environ[ 'HOME' ] = '/tmp/'
os.environ[ 'MPLCONFIGDIR' ] = '/tmp/'
import matplotlib
matplotlib.use('Agg')
from pylab import annotate
import pickle
import hashlib
import pymysql
import sys
import re
import xml.etree.ElementTree as ET
import xlrd
import xlwt
from xlutils.copy import copy

class DocManager(object):
    def __init__(self):
        self.new_docs = self.load_progress('new_docs.txt')#未处理集合
        self.old_docs = self.load_progress('old_docs.txt')#已处理集合
    def has_new_doc(self):
        '''
        判断是否有未处理的doc
        :return:
        '''
        return self.new_doc_size()!=0

    def get_new_doc(self):
        '''
        获取一个未处理的doc
        :return:
        '''
        new_doc = self.new_docs.pop()
        m = hashlib.md5()
        doc_data = open(new_doc, 'rb')
        m.update(doc_data.read())
        doc_data.close()
        self.old_docs.add(m.hexdigest())
        return new_doc

    def add_new_doc(self,doc):
        '''
         将新的doc添加到未处理的doc集合中
        :param doc:单个doc
        :return:
        '''
        if doc is None:
            return
        m = hashlib.md5()
        doc_data = open(doc, 'rb')
        m.update(doc_data.read())
        doc_data.close()
        doc_md5 =  m.hexdigest()
        if doc not in self.new_docs and doc_md5 not in self.old_docs:
            self.new_docs.add(doc)
        return("ok")

    def add_new_docs(self,docs):
        '''
        将新的docs添加到未处理的doc集合中
        :param docs:doc集合
        :return:
        '''
        if docs is None or len(docs)==0:
            return
        for doc in docs:
            self.add_new_doc(doc)

    def new_doc_size(self):
        '''
        获取未处理doc集合的大小
        :return:
        '''
        return len(self.new_docs)

    def old_doc_size(self):
        '''
        获取已经处理doc集合的大小
        :return:
        '''
        return len(self.old_docs)

    def save_progress(self,path,data):
        '''
        保存进度
        :param path:文件路径
        :param data:数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self,path):
        '''
        从本地文件加载进度
        :param path:文件路径
        :return:返回set集合
        '''
        print ('[+] 从文件加载进度: %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print ('[!] 无进度文件, 创建: %s' % path)
        return set()

def insert2db(tp):
    # 打开数据库连接
    db = pymysql.connect("localhost","root","root","yinjiang",charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO rheo(编号, \
           EtaMax, GPMax, GP5, GP10, Eta100, Eta200, Eta300, 剪切速率5与10粘度比, 剪切速率10与100粘度比) \
           VALUES ('%s', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f')" % \
           (tp[0], tp[1], tp[2], tp[3], tp[4], tp[5], tp[6], tp[7], tp[8], tp[9])    
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 执行sql语句
       db.commit()
       print ("Data insert successfully!")
    except:
       # 发生错误时回滚
       db.rollback()
    # 关闭数据库连接
    db.close()
    
def changetotxt(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            nroot = os.path.join(parent,filename)
            if '.xml' in nroot:
                fullpath = nroot.replace('\\','/')         #得到文件完整路径
                newname = fullpath.replace('.xml','.txt')
                os.rename(fullpath,newname)
    return rootdir

def changetoutf8(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            nroot = os.path.join(parent,filename)
            if '.txt' in nroot:
                fullpath = nroot.replace('\\','/')         #得到文件完整路径  
                f = open (fullpath, "r",encoding = 'utf-8',errors = 'ignore')
                con = f.read()
                if 'encoding' not in con:
                    open(fullpath, 'w+',encoding = 'utf-8').write(re.sub(r'xml version="1.0"', r'xml version="1.0"  encoding="UTF-8"', con))

def changetoxml(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            nroot = os.path.join(parent,filename)
            if '.txt' in nroot:
                fullpath = nroot.replace('\\','/')         #得到文件完整路径  
                newname = fullpath.replace('.txt','.xml')
                os.rename(fullpath,newname)

def changetoxls(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            nroot = os.path.join(parent,filename)
            if '.xml' in nroot:
                fullpath = nroot.replace('\\','/')         #得到文件完整路径
                fullpathxls = nroot.replace('.xml','.xls')
                tree = ET.parse(fullpath)
                root1 = tree.getroot()
                n = 0
                file = xlwt.Workbook()  #创建一个工作簿
                table = file.add_sheet('sheet 1')  #创建一个工作表
                table.write(0,1,'GP in 1/s')
                table.write(0,2,'Tau in Pa')
                table.write(0,3,'Eta in mPas')
                table.write(0,4,'T in oC')
                table.write(0,5,'t in s')
                table.write(0,6,'t_seg in s')   #写入表头
                if 'mPas'in root1[3][0][0][3][0].text:
                    changeunit = 1
                else:
                    changeunit = 1000
                for data in root1.iter(root1[3][0][0][0][0].tag):
                    if n>6 and (n%7)==3:
                        table.write(n//7, n%7, float(data.text)*changeunit)  #写入
                    elif n>6 and (n%7)!=0 and (n%7)!=3:
                        table.write(n//7, n%7, float(data.text))  #写入
                    elif n>6:
                        table.write(n//7, n%7, data.text)
                    n+=1
                file.save(fullpathxls)  #保存

def calculate(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            nroot1 = os.path.join(parent,filename)
            nroot = nroot1.replace('\\','/')
            if '.xls' in nroot and '汇总' not in nroot:
                data = xlrd.open_workbook(nroot)
                sheet1 = data.sheet_by_index(0)
                
                if sheet1.nrows > 300:
                    EtaMax = 0
                    for j in range(1,301):
                        if float(sheet1.cell(j,3).value) > EtaMax:
                            EtaMax = float(sheet1.cell(j,3).value)
                            GPMax = float(sheet1.cell(j,1).value)
                    a = 0
                    for i1 in range(2,301):
                        if float(sheet1.cell(i1,1).value) > 10 and a == 0:
                            GP10 = float(sheet1.cell(i1,3).value) - (float(sheet1.cell(i1,3).value) - float(sheet1.cell(i1-1,3).value))/(float(sheet1.cell(i1,1).value) - float(sheet1.cell(i1-1,1).value)) * (float(sheet1.cell(i1,1).value)-10)
                            a+=1
                            
                    b=0
                    for i2 in range(2,301):
                        if float(sheet1.cell(i2,1).value) > 5 and b == 0:
                            GP5 = float(sheet1.cell(i2,3).value) - (float(sheet1.cell(i2,3).value) - float(sheet1.cell(i2-1,3).value))/(float(sheet1.cell(i2,1).value) - float(sheet1.cell(i2-1,1).value)) * (float(sheet1.cell(i2,1).value)-5)
                            b+=1
                    Eta100 = float(sheet1.cell(100,3).value)
                    Eta200 = float(sheet1.cell(200,3).value)
                    Eta300 = float(sheet1.cell(300,3).value)
                    bkcopy = copy(data)
                    shcopy = bkcopy.get_sheet(0)
                    
                    if EtaMax:
                        shcopy.write(1,8,EtaMax)
                    if GPMax:
                        shcopy.write(1,9,GPMax)
                    if GP5:
                        shcopy.write(1,10,GP5)
                    if GP10:
                        shcopy.write(1,11,GP10)
                    if Eta100:
                        shcopy.write(1,12,Eta100)
                    if Eta200:
                        shcopy.write(1,13,Eta200)
                    if Eta300:
                        shcopy.write(1,14,Eta300)
                    bkcopy.save(nroot)  #保存

def addall(rootdir):
    GPmax = 0
    file_path = rootdir.replace('\\','/')+'/流变汇总.xls'
    if not os.path.exists(file_path):
        file = xlwt.Workbook()  #创建一个工作簿
        table = file.add_sheet('sheet 1')  #创建一个工作表
        table.write(0,0,'文件编号')
        table.write(0,1,'EtaMax (mPas)')
        table.write(0,2,'GPMax (1/s)')
        table.write(0,3,'GP5 (mPas)')
        table.write(0,4,'GP10 (mPas)')
        table.write(0,5,'Eta100 (mPas)')
        table.write(0,6,'Eta200 (mPas)')
        table.write(0,7,'Eta300 (mPas)')
        table.write(0,8,'剪切速率5与10粘度比')
        table.write(0,9,'剪切速率10与100粘度比')
        file.save(file_path)
        print('汇总文件' + file_path + '创建成功!') 
    else:
        print('汇总文件已存在')    
    bk1 = xlrd.open_workbook(file_path) #获取表格中已有行数
    sh1 = bk1.sheet_by_index(0)
    k = sh1.nrows
    bkcopy1 = copy(bk1)
    shcopy1 = bkcopy1.get_sheet(0) 
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            nroot1 = os.path.join(parent,filename)
            nroot = nroot1.replace('\\','/')
            file_name = filename.replace('.xls','').replace('-','')
            if '.xls' in nroot and '汇总' not in nroot:
                data = xlrd.open_workbook(nroot)
                sheet1 = data.sheet_by_index(0)
                shcopy1.write(k,0,file_name)
                if float(sheet1.cell(1,8).value) > GPmax:
                    GPmax = float(sheet1.cell(1,8).value)
                try:
                    if sheet1.cell(1,8).value:
                        shcopy1.write(k,1,sheet1.cell(1,8).value)
                    if sheet1.cell(1,9).value:                    
                        shcopy1.write(k,2,sheet1.cell(1,9).value)
                    if sheet1.cell(1,10).value:                    
                        shcopy1.write(k,3,sheet1.cell(1,10).value)
                    if sheet1.cell(1,11).value:                    
                        shcopy1.write(k,4,sheet1.cell(1,11).value)
                    if sheet1.cell(1,12).value:                    
                        shcopy1.write(k,5,sheet1.cell(1,12).value)
                    if sheet1.cell(1,13).value:                    
                        shcopy1.write(k,6,sheet1.cell(1,13).value)
                    if sheet1.cell(1,14).value:                    
                        shcopy1.write(k,7,sheet1.cell(1,14).value)
                    shcopy1.write(k,8,float(sheet1.cell(1,10).value)/float(sheet1.cell(1,11).value))
                    shcopy1.write(k,9,float(sheet1.cell(1,11).value)/float(sheet1.cell(1,12).value))
                    bkcopy1.save(file_path)
                    k+=1#保存
                except:
                    print(nroot)          
    return GPmax
    
def drawpng(ROOTNOW, WIDTHL, WIDTHH):#nowdir为xml文件的路径
    rootdir = ROOTNOW + "/upload/all"
    xall = []
    yall = []
    name = []
    color = ["black","b","r","g","purple","olive","chocolate","deepskyblue","darkorange","lime","grey","royalblue"]
    cnames = {
        'aliceblue':            '#F0F8FF',
        'antiquewhite':         '#FAEBD7',
        'aqua':                 '#00FFFF',
        'aquamarine':           '#7FFFD4',
        'azure':                '#F0FFFF',
        'beige':                '#F5F5DC',
        'bisque':               '#FFE4C4',
        'black':                '#000000',
        'blanchedalmond':       '#FFEBCD',
        'blue':                 '#0000FF',
        'blueviolet':           '#8A2BE2',
        'brown':                '#A52A2A',
        'burlywood':            '#DEB887',
        'cadetblue':            '#5F9EA0',
        'chartreuse':           '#7FFF00',
        'chocolate':            '#D2691E',
        'coral':                '#FF7F50',
        'cornflowerblue':       '#6495ED',
        'cornsilk':             '#FFF8DC',
        'crimson':              '#DC143C',
        'cyan':                 '#00FFFF',
        'darkblue':             '#00008B',
        'darkcyan':             '#008B8B',
        'darkgoldenrod':        '#B8860B',
        'darkgray':             '#A9A9A9',
        'darkgreen':            '#006400',
        'darkkhaki':            '#BDB76B',
        'darkmagenta':          '#8B008B',
        'darkolivegreen':       '#556B2F',
        'darkorange':           '#FF8C00',
        'darkorchid':           '#9932CC',
        'darkred':              '#8B0000',
        'darksalmon':           '#E9967A',
        'darkseagreen':         '#8FBC8F',
        'darkslateblue':        '#483D8B',
        'darkslategray':        '#2F4F4F',
        'darkturquoise':        '#00CED1',
        'darkviolet':           '#9400D3',
        'deeppink':             '#FF1493',
        'deepskyblue':          '#00BFFF',
        'dimgray':              '#696969',
        'dodgerblue':           '#1E90FF',
        'firebrick':            '#B22222',
        'floralwhite':          '#FFFAF0',
        'forestgreen':          '#228B22',
        'fuchsia':              '#FF00FF',
        'gainsboro':            '#DCDCDC',
        'ghostwhite':           '#F8F8FF',
        'gold':                 '#FFD700',
        'goldenrod':            '#DAA520',
        'gray':                 '#808080',
        'green':                '#008000',
        'greenyellow':          '#ADFF2F',
        'honeydew':             '#F0FFF0',
        'hotpink':              '#FF69B4',
        'indianred':            '#CD5C5C',
        'indigo':               '#4B0082',
        'ivory':                '#FFFFF0',
        'khaki':                '#F0E68C',
        'lavender':             '#E6E6FA',
        'lavenderblush':        '#FFF0F5',
        'lawngreen':            '#7CFC00',
        'lemonchiffon':         '#FFFACD',
        'lightblue':            '#ADD8E6',
        'lightcoral':           '#F08080',
        'lightcyan':            '#E0FFFF',
        'lightgoldenrodyellow': '#FAFAD2',
        'lightgreen':           '#90EE90',
        'lightgray':            '#D3D3D3',
        'lightpink':            '#FFB6C1',
        'lightsalmon':          '#FFA07A',
        'lightseagreen':        '#20B2AA',
        'lightskyblue':         '#87CEFA',
        'lightslategray':       '#778899',
        'lightsteelblue':       '#B0C4DE',
        'lightyellow':          '#FFFFE0',
        'lime':                 '#00FF00',
        'limegreen':            '#32CD32',
        'linen':                '#FAF0E6',
        'magenta':              '#FF00FF',
        'maroon':               '#800000',
        'mediumaquamarine':     '#66CDAA',
        'mediumblue':           '#0000CD',
        'mediumorchid':         '#BA55D3',
        'mediumpurple':         '#9370DB',
        'mediumseagreen':       '#3CB371',
        'mediumslateblue':      '#7B68EE',
        'mediumspringgreen':    '#00FA9A',
        'mediumturquoise':      '#48D1CC',
        'mediumvioletred':      '#C71585',
        'midnightblue':         '#191970',
        'mintcream':            '#F5FFFA',
        'mistyrose':            '#FFE4E1',
        'moccasin':             '#FFE4B5',
        'navajowhite':          '#FFDEAD',
        'navy':                 '#000080',
        'oldlace':              '#FDF5E6',
        'olive':                '#808000',
        'olivedrab':            '#6B8E23',
        'orange':               '#FFA500',
        'orangered':            '#FF4500',
        'orchid':               '#DA70D6',
        'palegoldenrod':        '#EEE8AA',
        'palegreen':            '#98FB98',
        'paleturquoise':        '#AFEEEE',
        'palevioletred':        '#DB7093',
        'papayawhip':           '#FFEFD5',
        'peachpuff':            '#FFDAB9',
        'peru':                 '#CD853F',
        'pink':                 '#FFC0CB',
        'plum':                 '#DDA0DD',
        'powderblue':           '#B0E0E6',
        'purple':               '#800080',
        'red':                  '#FF0000',
        'rosybrown':            '#BC8F8F',
        'royalblue':            '#4169E1',
        'saddlebrown':          '#8B4513',
        'salmon':               '#FA8072',
        'sandybrown':           '#FAA460',
        'seagreen':             '#2E8B57',
        'seashell':             '#FFF5EE',
        'sienna':               '#A0522D',
        'silver':               '#C0C0C0',
        'skyblue':              '#87CEEB',
        'slateblue':            '#6A5ACD',
        'slategray':            '#708090',
        'snow':                 '#FFFAFA',
        'springgreen':          '#00FF7F',
        'steelblue':            '#4682B4',
        'tan':                  '#D2B48C',
        'teal':                 '#008080',
        'thistle':              '#D8BFD8',
        'tomato':               '#FF6347',
        'turquoise':            '#40E0D0',
        'violet':               '#EE82EE',
        'wheat':                '#F5DEB3',
        'white':                '#FFFFFF',
        'whitesmoke':           '#F5F5F5',
        'yellow':               '#FFFF00',
        'yellowgreen':          '#9ACD32'}
    morecolor = []
    for key in cnames:
        morecolor.append(cnames[key])
    #print(morecolor)    
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            list1=os.path.join(parent,filename)
            nowdir=list1.replace('\\','/')
            if '.xls' in nowdir and '汇总' not in nowdir:
                labelname = filename.replace(".xls",'')
                name.append(labelname)
                data = xlrd.open_workbook(nowdir)
                sheet1 = data.sheet_by_index(0)
                x = []
                y = []
                for i in range(WIDTHL, WIDTHH):
                    if float(sheet1.cell(i,1).value)>0 and float(sheet1.cell(i,3).value)>0:
                        x.append(float(sheet1.cell(i,1).value))
                        y.append(float(sheet1.cell(i,3).value))
                xall.append(x)
                yall.append(y)
                # 删除xls文档
                #os.remove(nowdir)
                #print("xls文件删除成功！")
    # 通过rcParams设置全局横纵轴字体大小
    matplotlib.pyplot.rcParams['font.sans-serif']=['Arial']
    matplotlib.rcParams['xtick.direction'] = 'in' 
    matplotlib.rcParams['ytick.direction'] = 'in' 
    matplotlib.rcParams['xtick.labelsize'] = 12
    matplotlib.rcParams['ytick.labelsize'] = 12
    font = {'family' : 'Arial',
        'color'  : 'black',
        'weight' : 'normal',
        'size'   : 16,
        }
            
    matplotlib.pyplot.figure('IV Curve',figsize=(6,4.5))
    ax = matplotlib.pyplot.subplot(1,1,1)
    ax.spines['bottom'].set_linewidth(1.3)
    ax.spines['left'].set_linewidth(1.3)
    ax.spines['top'].set_linewidth(1.3)        
    ax.spines['right'].set_linewidth(1.3)
    # 通过'k'指定线的颜色，lw指定线的宽度
    # 第三个参数除了颜色也可以指定线形，比如'r--'表示红色虚线
    # 更多属性可以参考官网：http://matplotlib.org/api/pyplot_api.html
    if len(name) < 13:
        lenth = len(name)
        for i in range(lenth):
            matplotlib.pyplot.plot(xall[i], yall[i], color[i], lw=2,label = name[i])
    else:
        lenth = len(name)
        for i in range(lenth):
            matplotlib.pyplot.plot(xall[i], yall[i], morecolor[i], lw=2,label = name[i])
    #matplotlib.pyplot.xlim(0, widthh)
    matplotlib.pyplot.xlabel('GP (1/s)',fontdict=font)
    #matplotlib.pyplot.ylim(0, heighth)
    matplotlib.pyplot.ylabel('Eta (mPas)',fontdict=font)
    # scatter可以更容易地生成散点图
    #matplotlib.pyplot.scatter(x, y)
    matplotlib.pyplot.grid(False)
    matplotlib.pyplot.legend()
    # 将当前figure的图保存到文件
    npath = ROOTNOW + "/pythonscript/png/RheoCurve.png"
    print(npath+"图片保存成功！")
    matplotlib.pyplot.savefig(npath, bbox_inches='tight', dpi=300)

def returnall(nowdir, file_name):
    data=xlrd.open_workbook(nowdir)
    sheet1=data.sheet_by_index(0)
    return(file_name, float('%.4f' %sheet1.cell(1,8).value), float('%.4f' %sheet1.cell(1,9).value),\
    float('%.4f' %sheet1.cell(1,10).value), float('%.4f' %sheet1.cell(1,11).value), float('%.4f' %sheet1.cell(1,12).value),\
    float('%.4f' %sheet1.cell(1,13).value), float('%.4f' %sheet1.cell(1,14).value), \
    float('%.4f' %(float(sheet1.cell(1,10).value)/float(sheet1.cell(1,11).value))), \
    float('%.4f' %(float(sheet1.cell(1,11).value)/float(sheet1.cell(1,12).value))))

    
def insertall(ROOTNOW):
    rootdir = ROOTNOW + "/upload/all"
    docmanager = DocManager()
    
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        
            nowdir = os.path.join(parent,filename).replace('\\','/')
            #print(nowdir)
            file_name = filename.replace('.xls','').replace('-','')
            if '.xls' in nowdir and '汇总' not in nowdir:
                data = returnall(nowdir, file_name)
                print(data)
                docmanager.add_new_doc(nowdir)
                if docmanager.has_new_doc():
                    print("有新数据可以插入")
                    rt = docmanager.get_new_doc()
                    if data:
                        try:
                            insert2db(data)
                        except:
                            print("数据已经存在于数据库中!")
                    else:
                        print("返回空值")
                else:
                    print("数据已经存在于数据库中!")
                os.remove(nowdir)
                print("xls文件删除成功！")
                
    docmanager.save_progress('new_docs.txt',docmanager.new_docs)
    docmanager.save_progress('old_docs.txt',docmanager.old_docs)

def main(ROOTNOW, WIDTHL, WIDTHH):
    #xml改成txt增加一行encoding声明，后改回xml进行parse，输出成为xls
    root = ROOTNOW + "/upload/all"
    changetotxt(root)
    changetoutf8(root)
    changetoxml(root)
    changetoxls(root)
    #计算流变的几个特性数值，存入xls
    calculate(root)
    addall(root)
    #作图
    drawpng(ROOTNOW, WIDTHL, WIDTHH)
    #插入数据库
    insertall(ROOTNOW)   
    
#主程序
ROOTNOW = sys.path[0].replace('\\','/')
f = open(ROOTNOW+"/tmp/parameter.txt")
AREA = f.readline().split(' ')
if len(AREA) == 1:
    WIDTHL = 1
    WIDTHH = int(AREA[0])
    print("输入参数1")
elif len(AREA) == 2:
    WIDTHL = int(AREA[0])
    WIDTHH = int(AREA[1])
    print("输入参数2")
f.close()
 
main(ROOTNOW, WIDTHL, WIDTHH)
