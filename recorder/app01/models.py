# Create your models here.
from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        # user.is_superuser = True
        user.is_admin=True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64, verbose_name="姓名")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    # host_to_remote_user=models.ManyToManyField('HostToRemoteUser')
    department_groups=models.ForeignKey('DepartmentGroup',blank=True,null=True,on_delete='')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email
    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    def __str__(self):              # __unicode__ on Python 2
        return self.email

class DepartmentGroup(models.Model):
    '''部门分组'''
    # department_choices=((0,'行领导'),(1,'办公室'),(2,'金融管理部'),(3,'国库会计部'))
    # department=models.SmallIntegerField(choices=department_choices,blank=True,null=True,verbose_name='部门')
    department=models.CharField(max_length=64,verbose_name='部门')
    head=models.OneToOneField('UserProfile',blank=True,null=True,verbose_name='负责人',on_delete='')

    def __str__(self):
        return '%s'%self.department

class Standard(models.Model):
    '''费用标准，时间标准'''
    cost=models.SmallIntegerField(verbose_name='费用标准')
    morning=models.CharField(max_length=32,verbose_name='上午上班')
    noon=models.CharField(max_length=32,verbose_name='上午下班')
    afternoon=models.CharField(max_length=32,verbose_name='下午上班')
    night=models.CharField(max_length=32,verbose_name='下午下班')
    go_to_work_time_error=models.CharField(max_length=32,verbose_name='上班时间误差')
    go_off_work_time_error=models.CharField(max_length=32,verbose_name='下班时间误差')


class FileStore(models.Model):
    '''文件储存地址、时间'''
    file_addre=models.CharField(max_length=64,default='app01/file/',verbose_name='文件储存地址')
    file_time=models.CharField(max_length=32,verbose_name='文件日期')
    file_format_choices=((0,'xls'),(1,'csv'),(2,'json'),(3,'txt'))
    file_format=models.SmallIntegerField(default=0,verbose_name='文件格式')
    file_data_summary=models.BooleanField(default=False,verbose_name='数据汇总')
    def __str__(self):
        return self.file_time

class Detailed(models.Model):
    '''每个用户考勤详细情况'''
    user=models.CharField(max_length=64)
    file_stores_id=models.ForeignKey('FileStore',on_delete=models.CASCADE)
    data=models.CharField(max_length=32,verbose_name='数据日期')
    detail=models.CharField(max_length=64,verbose_name='详细')
    def __str__(self):
        return self.user

class Summary(models.Model):
    '''对考勤表进行汇总'''
    user=models.ForeignKey('UserProfile',on_delete='')
    file_stores_id=models.ForeignKey('FileStore',on_delete='')
    date=models.DateTimeField(auto_now_add=True)
    lack=models.SmallIntegerField(verbose_name='缺少次数')
    explain=models.TextField(verbose_name='解释说明')
    fine=models.CharField(max_length=64,verbose_name='罚金')
    def __str__(self):
        return '%s %s'%(self.user,self.fine)
class Approval(models.Model):
    '''审批'''
    pass