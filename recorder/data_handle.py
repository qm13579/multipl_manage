import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recorder.settings")
import django
django.setup()

from app01 import models

class DataTatol(object):
    '''数据汇总'''
    def __init__(self):
        self.handle=[]
    def data_summary_judge(self):
        '''判断数据是否进行汇总处理'''
        #可能存在多个数据
        wait_handles=models.FileStore.objects.filter(file_data_summary=False)
        if wait_handles:
            handle_dict={}
            for query in wait_handles:
                handle_dict['query']=query
                handle_dict['id']=query.id
                self.handle.append(handle_dict)
    def data_summary_handle(self):
        '''对数据进行汇总处理'''
        self.data_summary_judge()
        if self.handle:
            for query in self.handle:
                print (query)
                wait_handle_data=models.Detailed.objects.filter(file_stores_id_id=query['id'])
                obj=HandelDate(wait_handle_data)
                data=obj.handle()
                return data,query['query']
        else:
            print ('无数据汇总')
    def model_store(self):
        data,query=self.data_summary_handle()
        print(data)
        summary_list = []
        for dict_key_user in data :
            user=dict_key_user['user']
            count_str=None
            val_str=None
            count_str='Blank/Lack:%s/%s'%(dict_key_user['val']['blank']['count'],dict_key_user['val']['lack']['count'])
            val_str='Blank/Lack:%s/%s'%(';'.join(dict_key_user['val']['blank']['val']),dict_key_user['val']['lack']['val'])
            summary_list.append(models.Summary(user=user,
                                               file_stores_id_id=query.id,
                                               lack_detail=val_str,
                                               lack_count=count_str,
                                               ))
        models.Summary.objects.bulk_create(summary_list)
        print ('数据汇总完成')

class HandelDate(object):
    def __init__(self,data):
        self.data = data#quertSet
        self.model = models.Standard.objects.all()
        self.cost = self.model.values('cost')[0]['cost']
        self.morning = int(''.join(self.model.values('morning')[0]['morning'].split(':')))
        self.noon = int(''.join(self.model.values('noon')[0]['noon'].split(':')))
        self.afternoon = int(''.join(self.model.values('afternoon')[0]['afternoon'].split(':')))
        self.night = int(''.join(self.model.values('night')[0]['night'].split(':')))
        self.go_off_work_time_error = int(self.model.values('go_off_work_time_error')[0]['go_off_work_time_error'])/60*100
        self.go_to_work_time_error = int(self.model.values('go_to_work_time_error')[0]['go_to_work_time_error'])/60*100
        self.info_summary_list = []  # 汇总列表
        self.info_summary_dict={}
        print (self.morning,self.noon,self.afternoon,self.night,self.go_off_work_time_error,self.go_to_work_time_error)
    def handle(self):
        info_blank_dict={}#用于None
        info_user=None
        info_blank=[] #信息None日期列表
        blank = 0
        info_lack=[]
        info_lack_dict={}
        lack=0
        total={}
        last_user=list(self.data)[-1]
        for query in self.data:
            #重置
            if info_user != query.user:
                if info_blank:
                    #把None值进行字典化
                    info_blank_dict['val']=info_blank
                    info_blank_dict['count']=blank
                    #把缺失值进行字典化
                    info_lack_dict['val']=';'.join(info_lack)
                    info_lack_dict['count']=lack
                    self.info_summary_dict['blank']=info_blank_dict
                    self.info_summary_dict['lack']=info_lack_dict
                    total['user']=info_user
                    total['val']=self.info_summary_dict
                    self.info_summary_list.append(total)
                info_user=query.user
                info_blank_dict={}
                info_blank=[]
                blank = 0
                info_lack = []
                info_lack_dict = {}
                lack = 0
                total = {}
                self.info_summary_dict={}

            #判断值为nan还是字符串值
            if query.detail=='nan':
                blank+=1
                info_blank.append(query.data)
            else:
                date_handel=self.date_handle(query)
                if type(date_handel)== bool:
                    pass
                else:
                    lack+=date_handel['count']
                    info_lack.append(query.data+'-'+'|'.join(date_handel['val']))
                    # print ('次数:',date_handel['count'],'时段:',date_handel['val'],'日期:',query.data)
        # 当前用户为最后一个用户
        if info_blank:
            # 把None值进行字典化
            info_blank_dict['val'] = info_blank
            info_blank_dict['count'] = blank
            # 把缺失值进行字典化
            info_lack_dict['val'] = ';'.join(info_lack)
            info_lack_dict['count'] = lack
            self.info_summary_dict['blank'] = info_blank_dict
            self.info_summary_dict['lack'] = info_lack_dict
            total['user'] = info_user
            total['val'] = self.info_summary_dict
            self.info_summary_list.append(total)
        return self.info_summary_list
    def date_handle(self,query):
        '''日期处理'''
        # print (query.detail, query.data, query.user)
        morning=False
        noon=False
        afternoon=False
        night=False
        date=query.data
        time_list=query.detail.split('|')
        for i in time_list:
            time_int=int(''.join(i.split(':')))
            if self.morning-self.go_to_work_time_error<time_int<self.morning:
                morning=True
            elif self.noon<=time_int<self.noon+self.go_off_work_time_error:
                noon=True
            elif self.afternoon-self.go_to_work_time_error<=time_int<=self.afternoon:
                afternoon=True
            elif self.night<=time_int<=self.night+self.go_off_work_time_error:
                night=True
        if all((morning,noon,afternoon,night)):
            return True
        else:
            date_str=['morning','noon','afternoon','night']
            date_dict={}
            date_list=[]
            count=0
            for i, j in enumerate([morning, noon, afternoon, night]):
                if not j:
                    date_list.append(date_str[i])
                    count+=1
            return {'count':count,'val':date_list}
if __name__ == '__main__':
    import time
    now=time.time()
    obj = DataTatol()
    obj.model_store()
    print (time.time()-now)

#{user,xxx,val:[{blank:{blank:10,val:[]}}]}