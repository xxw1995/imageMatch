# _*_ coding=utf-8 _*_
__date__ = '9/24/2018 13:22 '

import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
#配置项文件
from config import *
from utils import getColorVec

import  pymysql

db = pymysql.connect(DB_addr,DB_user,DB_passwod,DB_name )

#读取folderPath下的所有文件
def readFileInCurrentFolder(folderPath):
    all=os.listdir(folderPath)
    files=[]
    for file in  all:
        if not os.path.isdir(file):
            files.append(file)
    return files


def WriteDb(filename):
    if filename!="":
        fileSet=[filename]
    else:
        fileSet=readFileInCurrentFolder(FOLDER)
    ISFORMAT="%Y-%m-%d %H:%M:%S"
    maxToCommit=0
    cursor=db.cursor()
    start_time=time.time()
    for file in fileSet:
        img=cv2.imread(FOLDER+file)
        if img.ndim !=3:
            raise RuntimeError("图像维数不为3")
        filestat=os.stat(FOLDER+file)
        modified_time_ori=time.localtime(filestat.st_mtime)
        modified_time= time.strftime(ISFORMAT, modified_time_ori)
        size=filestat.st_size
        colorVec=getColorVec(img)
        sqlstat="insert into ImageMatchInfo_fine (name, size, modified_time, featureValue) value (%s, %s, %s, %s)"
        #colorVecstr="".join(colorVec)
        colorVecstr=str()
        for one in colorVec:
            colorVecstr+=str(one)+","
        colorVecstr=colorVecstr.strip(',')
        toGetTuple=[file, size, modified_time, colorVecstr]
        try:
            cursor.execute(sqlstat, tuple(toGetTuple))
        except Exception as e:
            print(e)
        finally:
            #TODO::删掉下面一行
            db.commit()
            maxToCommit+=1
            if maxToCommit>50:
                db.commit()
                end_time=time.time()
                print(end_time-start_time, " s")
                start_time=end_time
                maxToCommit=0




if __name__ == '__main__':
    filename=input("请输入想要读的文件的路径, 不输入即读取"+FOLDER+"下的所有文件")
    WriteDb(filename)

