from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
# 커스텀 유저 모델을 사용하기 위해서는 BaseUserManager, AbstractBaseUser를 모두 구현해야 한다.
# BaseUserManager 클래스는 유저를 생성할 때 사용하는 헬퍼(Helper) 클래스이며, 
# 실제 모델(Model)은 AbstractBaseUser을 상속받아 생성하는 클래스입니다.
# 헬퍼(Helper) 클래스인 class UserManager(BaseUserManager):는 두 가지 함수를 가지고 있습니다.
# create_user(*username_field*, password=None, **other_fields)
# create_superuser(*username_field*, password, **other_fields)

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
      # username 필드와 REQUIRED_FIELDS의 필드가 모두 포함되어야 한다.
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
          email = self.normalize_email(email),
          username = username,
          password = password,
          first_name = first_name,
          last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required(필수라서 무조건 적어줘야한다.)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # 이메일로 로그인 하도록 설정
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # custom_user_model을 만들 때 필수적인거
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
