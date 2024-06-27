from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Visitor(models.Model):
    name = models.CharField(max_length=90)
    email = models.EmailField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tblvisitor"

class MyEmployeeManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(email, name, password, **extra_fields)

class Employee(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=90, unique=True)
    last_login = models.DateTimeField(blank=True, null=True)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')

    objects = MyEmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tblemployee"

class Visite(models.Model):
    visiteur = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    objet = models.CharField(max_length=90)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'myapp_visite'

class Courrier(models.Model):
    expediteur = models.CharField(max_length=100)
    destinataire = models.CharField(max_length=100)
    type_courrier = models.CharField(max_length=100)
    date_reception = models.DateField()
    reference_courrier = models.CharField(max_length=100)
    est_recu = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, default='en cours')

    def __str__(self):
        return self.reference_courrier
