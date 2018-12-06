import pandas as pd
import re
import numpy as np
import time
import sys, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recorder.settings")
import django
django.setup()


def handle(data,df):
    '''处理每一个变量数据'''
    columns=[column for column in df.columns]
    vals=[va for va in data]
    val_list=[]
    for val,index in zip(vals,columns):
        key={}
        if str(val) != 'nan':
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
    name_index=None
    for index in df.index:
        if index%2==0:
            info_dict={}
            info_dict['name']=df.ix[index][9]
            if str(info_dict['name'])=='nan':
                info_dict['name'] = df.ix[index][8]
            # print(info_dict['name'])
        else:
            info_dict['val']=handle(df.ix[index],df)
        if info_dict.get('val'):
            info_list.append(info_dict)
    return info_list

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
    # print('差集:',file_list-model_fiel)
    # print ('交集:',file_list&model_fiel)
    #应该取数据库文件文件列表的差集
    difference_set = []
    if len(file_list-model_fiel)!=0:
        for file in file_list-model_fiel:
            file_store = {}
            print(file)
            file_store['val']=file_data(file)
            file_store['date']=file
            difference_set.append(file_store)
        # print(difference_set)
        return difference_set
    return difference_set
def mode_store():
    #父表录入
    difference_set=file_check()
    if difference_set:
        from app01 import models
        for file_dict in difference_set:
            obj=models.FileStore.objects.create(
                file_time=file_dict['date']
            )
            #字表录入
            task_log=[]
            for item in file_dict['val']:
                for j in item['val']:
                    task_log.append(models.Detailed( user=item['name'],file_stores_id_id=obj.id,data=j['index'],detail=j['val']))
            models.Detailed.objects.bulk_create(task_log)
        print('共计%s组数据已入库'%len(difference_set))
    else:
        print('无新数据')
if __name__ == '__main__':
    now_time = time.time()
    # file_data('2018-11')
    file_check()
    # mode_store()
    print(time.time() - now_time)