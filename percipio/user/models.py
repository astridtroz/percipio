from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, name ,user_type, password=None, password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, user_type, password=None, password2=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            user_type=user_type
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    USER_TYPE_CHOICES=(
        ('contributor', 'Contributor'),
        ('provider', 'Provider'),
    )
    name=models.CharField(max_length=100)
    user_type= models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','user_type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return  self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

    
    



class Provider(models.Model):
    user_obj= models.OneToOneField(MyUser,on_delete=models.CASCADE)
    project_decription= models.TextField(max_length=100)

    def __str__(self):
        return self.user_obj.email
    

class Contributor(models.Model):
    user_obj=models.OneToOneField(MyUser, on_delete=models.CASCADE)
    skills=models.TextField(max_length=100)
    

    def __str__(self):
        return self.user_obj.email
