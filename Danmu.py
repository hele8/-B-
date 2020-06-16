
import sys
import os
import csv
import re
import wordcloud
import requests
from lxml import etree
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout,QLabel,QGridLayout, QApplication,QLineEdit,QFileDialog)



class Danmu(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()


    def initUI(self):

        self.review=QLineEdit(self)
        self.file=QLineEdit(self)
        self.outfile=QLineEdit(self)
        self.pic=QLineEdit(self)
        self.danmu=QLabel(self)
        self.lb = QLabel(self)


        btn=QPushButton("获取视频号")
        getbtn=QPushButton("爬取弹幕")
        cloudbtn=QPushButton("生成云图")
        filebtn=QPushButton("打开文件夹")
        outfilebtn=QPushButton("文件名")
        picbtn=QPushButton("图片名")
        #review.textChanged[str].connect(self.onChanged)

        grid=QGridLayout()
        grid.setSpacing(5)

 
        grid.addWidget(btn, 1, 0)
        grid.addWidget(self.review,1,1)

        grid.addWidget(filebtn,2,0)
        grid.addWidget(self.file,2,1)
        grid.addWidget(outfilebtn,3,0)
        grid.addWidget(self.outfile,3,1)
        grid.addWidget(picbtn,4,0)
        grid.addWidget(self.pic, 4, 1)



        grid.addWidget(getbtn, 5, 0)
        grid.addWidget(self.danmu,5,1)
        grid.addWidget(cloudbtn, 6, 0)
        grid.addWidget(self.lb,6,1,4,1)



        btn.clicked.connect(self.addNum)
        getbtn.clicked.connect(self.get_Danmu1)
        cloudbtn.clicked.connect(self.Getcloud)
        filebtn.clicked.connect(self.openFile)
        outfilebtn.clicked.connect(self.get_name)
        #picbtn.clicked.connect(self.getpic_name)

        self.setLayout(grid)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('爬取弹幕小工具')
        self.show()

    def addNum(self):
        self.name = self.review.text()
        print(self.name)
    def get_Danmu1(self):
        self.danmu.setText("开始爬取弹幕")
        BVname=self.review.text()
        file1=self.file.text()
        file=os.path.join(file1,self.outfile.text())
        #print(file)
        spider = BiliSpider(BVname,file)
        #print(spider)
        spider.run()
        self.danmu.setText("爬取成功！！！！")


    def openFile(self):
        get_directory_path = QFileDialog.getExistingDirectory(self,
                                                              "选取指定文件夹",
                                                              "D:/")
        self.file.setText(str(get_directory_path))
    def Getcloud(self):
        #BVname = self.review.text()
        file2 = self.file.text()
        file3 = os.path.join(file2, self.outfile.text())
        picpath = os.path.join(file2, self.pic.text())
        Create_CD(self,file3,picpath)
        self.lb.setPixmap(QPixmap(picpath))

    def get_name(self):
        self.filename=self.outfile.text()
        print(self.filename)




class BiliSpider:
    # 弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造

    def __init__(self, BV,FilePath):
        # 构造要爬取的视频url地址

        self.BVurl = "https://m.bilibili.com/video/" + BV

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}
        self.path=FilePath

    def getXml_url(self):

        # 获取该视频网页的内容

        response = requests.get(self.BVurl, headers = self.headers)

        html_str = response.content.decode()

        # 使用正则找出该弹幕地址

        # 格式为：https://comment.bilibili.com/168087953.xml

        # 我们分隔出的是地址中的弹幕文件名，即 168087953

        getWord_url =re.findall(r'"cid":[\d]*',html_str)
       # print(getWord_url)

        getWord_url = getWord_url[0].replace('"cid":',"").replace(" ","")

        # 组装成要请求的xml地址

        xml_url = "https://comment.bilibili.com/{}.xml".format(getWord_url)

        return xml_url
#https://comment.bilibili.com/173527223.xml


    # Xpath不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本

    def parse_url(self,url):

        response = requests.get(url,headers = self.headers)

        return response.content



    # 弹幕包含在xml中的<d></d>中，取出即可

    def get_word_list(self,str):
        #format = re.compile("<d.*?>(.*?)</d>")
        #DanMu = format.findall(xml_url)

        html = etree.HTML(str)

        word_list = html.xpath("//d/text()")

        return word_list



    def run(self):

        # 1.根据BV号获取弹幕的地址

        start_url = self.getXml_url()

        # 2.请求并解析数据

        xml_str = self.parse_url(start_url)

        word_list = self.get_word_list(xml_str)
        print(len(word_list))

        # 3.打印

        for word in word_list:

            #file='D:/Desktop'


            print(word)
            #filepath=self.path+'/Danmu7.csv'
            #print(filepath)
            with open(self.path, "a", newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                danmu = []
                danmu.append(word)
                writer.writerow(danmu)

def Create_CD(self,path1,path2):
    self.mypath=path1
    f = open(self.mypath , encoding='utf-8')
    txt = f.read()

    # 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc')

    # 将txt变量传入w的generate()方法，给词云输入文字
    w.generate(txt)

    # 将词云图片导出到当前文件夹
    self.mypath2=path2
    w.to_file(self.mypath2)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex=Danmu()
    sys.exit(app.exec_())

