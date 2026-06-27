from django.db import models

# Create your models here.
class sign_up(models.Model):
    email=models.EmailField(max_length=50,default='')
    password=models.CharField(max_length=6,default='')
    conf_pass=models.CharField(max_length=6,default='')
    deposit=models.PositiveIntegerField(default=0)
    name=models.CharField(max_length=10,default='')
    contact=models.CharField(max_length=10,default='')
    account_no=models.CharField(max_length=16,default='')

class loan_type(models.Model):
    loan_name=models.CharField(max_length=50,default='')
    rate=models.FloatField(default=0)

class loan_detail(models.Model):
    loan_name=models.CharField(max_length=30,default='')
    amount=models.PositiveIntegerField(max_length=30,default='')
    year=models.FloatField(max_length=10,default='')
    rate=models.FloatField(default='')
    total_amt=models.PositiveBigIntegerField(max_length=30,default='')
    emi=models.FloatField(default=0)
    account_no=models.CharField(max_length=16,default='')

# class emi_detail(models.Model):
#     loan_name=models.CharField(max_length=30,default='')
#     amount=models.PositiveIntegerField(max_length=30,default='')
#     year=models.FloatField(max_length=10,default='')
#     rate=models.FloatField(default='')
#     total_amt=models.PositiveBigIntegerField(max_length=30,default='')
#     emi=models.FloatField(default=0)

class loan_emi(models.Model):
    emi_id=models.PositiveBigIntegerField(default=0,null=True, blank=True)
    EMI=models.PositiveBigIntegerField(default=0)
    p_amt=models.PositiveBigIntegerField(default=0)
    interest=models.PositiveBigIntegerField(default=0)
    balance=models.PositiveBigIntegerField(default=0)
    account_no=models.PositiveBigIntegerField(default=0)
    l_name=models.CharField(max_length=30,default='')