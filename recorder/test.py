import pandas as pd
import re
import numpy as np
import time
now_time=time.time()
# df=pd.read_excel('app01/file/2018-10.xls',encoding='utf-8',skip_rows=1,header=3,index_col=False)
# print(df.index.values)
# print(df.ix[4][9])
print('======')
# print(df)
# print(df.ix[0])

def handle(data,df):
    '''处理每一个变量数据'''
    columns=[column for column in df.columns]
    vals=[va for va in data]
    val_list=[]
    for val,index in zip(vals,columns):
        key={}
        if str(val) != 'nan':
            key['index']='|'.join(re.findall('\d\d:\d\d',val))
            key['val']=val
        else:
            key['index']=index
            key['val']=val
        val_list.append(key)
    return val_list

def file_data(file):
    '''读取文件,进行数据传递'''
    df=pd.read_excel('app01/file/%s.xls'%file,encoding='utf-8',skip_rows=1,header=3,index_col=False)
    info_list=[]
    for index in df.index:
        if index%2==0:
            info_dict={}
            info_dict['name']=df.ix[index][9]
        else:
            info_dict['val']=handle(df.ix[index],df)
        if info_dict.get('val'):
            info_list.append(info_dict)
    return info_list

import os
#打开文件
#文件下的所有文件
def file_check():
    '''检查文件是否缺失，'''
    files=os.listdir('app01/file')
    data='%s-%s'%(time.localtime().tm_year,time.localtime().tm_mon)
    file_list=set()
    for file in files:
        file_list.add(re.findall('(\d+-\d+).*',file)[0])
    #获取数据库文件信息已存在的文件日期信息
    # from app01 import models
    model_fiel=set(['2018-08','2018-09'])
    # print(file_list,model_fiel)
    if len(model_fiel&file_list)==0:
        for file in file_list:
            file_store = {}
            file_store['val']=file_data(file)
            file_store['date']=file
            print(file_store)

def mode_store(data):
    #父表录入

    #字表录入
    pass

file_check()
print(time.time()-now_time)



