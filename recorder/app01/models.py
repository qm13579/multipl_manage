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
    department_groups=models.ForeignKey('DepartmentGroup',blank=True,null=True,on_delete=models.CASCADE)
    role=models.ForeignKey('Role',blank=True,null=True,on_delete=models.CASCADE)
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

class Role(models.Model):
    name=models.CharField(max_length=64,unique=True)
    menus=models.ManyToManyField('Menus',blank=True)
    def __str__(self):
        return self.name

class DepartmentGroup(models.Model):
    '''部门分组'''
    department=models.CharField(max_length=64,verbose_name='部门')
    head=models.OneToOneField('UserProfile',blank=True,null=True,verbose_name='负责人',on_delete=models.CASCADE)

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
    file_format=models.SmallIntegerField(choices=file_format_choices,default=0,verbose_name='文件格式')
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
    user = models.CharField(max_length=64)
    file_stores_id=models.ForeignKey('FileStore',on_delete=models.CASCADE)
    lack_detail=models.CharField(max_length=246,verbose_name='缺少详细说明')
    lack_count=models.CharField(max_length=32,verbose_name='缺少次数')
    fine=models.CharField(max_length=64,verbose_name='罚金',blank=True,null=True)
    def __str__(self):
        return self.user

class Approval(models.Model):
    '''审批'''
    pass

class Menus(models.Model):
    '''动态菜单'''
    name = models.CharField(max_length=32, verbose_name='菜单')
    url_type_choices=((0,'absolute'),(1,'dynamic'))
    url_type=models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name=models.CharField(max_length=32,verbose_name='url')
    def __str__(self):
        return self.name
    class Meta:
        unique_together=('name','url_name')