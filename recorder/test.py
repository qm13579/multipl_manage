import pandas as pd
import re
import numpy as np
import time
import sys, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recorder.settings")
import django

django.setup()
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
            # key['index']='|'.join(re.findall('\d\d:\d\d',val))
            # key['val']=val
            key['index']=index
            key['val']='|'.join(re.findall('\d\d:\d\d',val))
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
    from app01 import models
    model_fiel=set()
    model_times=models.FileStore.objects.all().values('file_time')
    for i in model_times:
        model_fiel.add(i['file_time'])
    # print(file_list,model_fiel)
    # print (file_list&model_fiel)
    #应该取数据库文件文件列表的差集
    file_store=False
    if len(model_fiel&file_list)==0:
        for file in file_list:
            file_store = {}
            file_store['val']=file_data(file)
            file_store['date']=file
        return file_store
    return file_store
def mode_store():
    #父表录入
    file_dict=file_check()
    if file_dict:
        from app01 import models
        obj=models.FileStore.objects.create(
            file_time=file_dict['date']
        )
        #字表录入
        task_log=[]
        for item in file_dict['val']:
            for j in item['val']:
                task_log.append(models.Detailed( user=item['name'],file_stores_id_id=obj.id,data=j['index'],detai=j['val']))
        models.Detailed.objects.bulk_create(task_log)
        print('数据已入库')
    else:
        print('无新数据')
mode_store()
print(time.time()-now_time)
