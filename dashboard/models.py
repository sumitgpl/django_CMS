from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from multiselectfield import MultiSelectField

# Create your models here.

class Organization(models.Model):   
    orgname = models.CharField(max_length=100)    
    org_Img = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/default-img.png") 
    summary = models.CharField(max_length=200,default="")  
    user = models.OneToOneField(User, on_delete=models.CASCADE,default="1")
    MODULES_CHOICES = (
        ('businesscontinuity','businesscontinuity'),
        ('socialnetworks', 'socialnetworks'),
        ('contactcenter','contactcenter'),
        ('datacenter','datacenter'),
        ('videomn','videomn'),
        ('humanassets','humanassets'),
        ('hardware','hardware'),
        ('software','software'),
        ('cloud','cloud'),
        ('mobile','mobile'),
        ('security','security'),
        ('database','database'),
        ('connectivity','connectivity'),

    )    
    modules = MultiSelectField(choices=MODULES_CHOICES,default='businesscontinuity')
    class Meta:
        db_table = 'organization'
    def __str__(self):
        return self.orgname

class SMTPDetails(models.Model):
    host = models.CharField(max_length=50,default="")
    port = models.CharField(max_length=10,default="")
    username = models.CharField(max_length=50,default="")
    passwrd = models.CharField(max_length=50,default="")
    organizationid = models.IntegerField(default="0")
    def __str__(self):
        return 'SMTP Details'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizationid = models.IntegerField(default="0")
    name = models.CharField(max_length=20,default="",null=True, blank=True,)
    profile_pic = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/default-img.png") 
    grp = models.CharField(max_length=20,default="",null=True, blank=True,)
    jobtitle= models.CharField(max_length=20,default="",null=True, blank=True,)
    certificate = models.CharField(max_length=20,default="",null=True, blank=True,)
    yrexp = models.IntegerField(default="0") 
    salary= models.IntegerField(default="0") 
    alignmentscore = models.IntegerField(default="0")   
    def __str__(self):
        return self.user.username  

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
    
@receiver(post_save, sender=Organization)
def create_orgusermap(sender, instance, created, **kwargs):
    if created:
        p = Profile.objects.get(user=instance.user)
        p.organizationid = instance.id
        p.save()
        HumanAsset.objects.create(organizationid=instance.id,summary='summary')
        BusinessContinuity.objects.create(organizationid=instance.id,summary='summary')
        SMTPDetails.objects.create(organizationid=instance.id)

class ContactCenter(models.Model):
    organizationid = models.IntegerField(default="0") 
    name  = models.CharField(max_length=20,default="")
    contact_Img = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/default-img.png") 
    dateacquired = models.DateTimeField(default=datetime.now, blank=True)
    cost_of_acquisition = models.FloatField(null=True, blank=True, default=None)
    depreciation = models.CharField(max_length=20,default="")
    business_purpose = models.CharField(max_length=200,default="")
    owner = models.CharField(max_length=200,default="")
    recurrent_exp_perannum = models.FloatField(null=True, blank=True, default=None)
    location = models.CharField(max_length=20,default="")
    TYPE_CHOICES = (
        ('software','software'),
        ('hardware', 'hardware'),
        ('connectivity','connectivity'),
        ('other','other'),
    )    
    contype = models.CharField(max_length=20, choices=TYPE_CHOICES, default='software')  
    technical_details = models.CharField(max_length=200,default="")
    historical_cost = models.FloatField(null=True, blank=True, default=None)
    class Meta:
        db_table = 'ContactCenter'
    def __str__(self):
        return self.name

class ContactCenterFields(models.Model):
    contactcenter =  models.ForeignKey(ContactCenter, on_delete=models.CASCADE)
    fieldname = models.CharField(max_length=100)
    fieldvalue = models.CharField(max_length=100)
    def __str__(self):
        return self.fieldname


class AccessLog(models.Model):
    organizationid = models.IntegerField(default="0") 
    userid = models.IntegerField(default="0")
    pagename = models.CharField(max_length=50,default="")
    datetime = models.DateTimeField(blank=True)
    class Meta:
        db_table = 'accessLog'

class PostComments(models.Model): 
    organizationid = models.IntegerField(default="0") 
    commentid= models.IntegerField(default="0") 
    commentmsg = models.CharField(max_length=200,default="")
    filepath  = models.CharField(max_length=50,default="")
    commenttitle= models.CharField(max_length=50,default="")
    datetime= models.DateTimeField('datetime')

class PostCommentsUser(models.Model):
    organizationid = models.IntegerField(default="0") 
    commentid = models.IntegerField(default="0") 
    userid = models.IntegerField(default="0")
    class Meta:
        db_table = 'postcommentsuser'
  
class FinancialAnalysisData(models.Model): 
    organizationid  = models.IntegerField(default="0") 
    groupid  = models.IntegerField(default="0") 
    groupname = models.CharField(max_length=20)
    groupupdown = models.IntegerField(default="0",verbose_name ='Grow Percentage')
    subgroupid  = models.IntegerField(default="0") 
    subgroupname = models.CharField(max_length=20)
    subgroupcount = models.IntegerField(default="0") 
    amount  = models.DecimalField(default="0",decimal_places=2,max_digits=12) 
    prv_amount_1  = models.DecimalField(default="0",decimal_places=2,max_digits=12)
    prv_count_1 = models.IntegerField(default="0") 
    prv_amount_2  = models.DecimalField(default="0",decimal_places=2,max_digits=12) 
    prv_count_2 = models.IntegerField(default="0")
    prv_amount_3   = models.DecimalField(default="0",decimal_places=2,max_digits=12) 
    prv_count_3 = models.IntegerField(default="0")
    class Meta:
        db_table = 'financialanalysisdata'
    def __str__(self):
        return self.groupname        

class SocialNetwork(models.Model):
    organizationid  = models.IntegerField(default="0")
    twitterfollow  = models.CharField(max_length=200)
    twitterposts = models.CharField(max_length=200)
    twitterreplies = models.CharField(max_length=200)
    skypefollow  = models.CharField(max_length=200)
    skypeposts = models.CharField(max_length=200)
    skypereplies = models.CharField(max_length=200)
    linkedidfollow  = models.CharField(max_length=200)
    linkedidposts = models.CharField(max_length=200)
    linkedidreplies = models.CharField(max_length=200)   
    summary = models.CharField(max_length=200,default="") 
    class Meta:
        db_table = 'socialnetwork'       


class DatabaseDetails(models.Model):
    organizationid  = models.IntegerField(default="0")
    softwarecategory = models.CharField(max_length=20)
    sqldatabase = models.CharField(max_length=20)
    databaseversion = models.CharField(max_length=20)
    summary = models.CharField(max_length=200)
    db_Img = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/database.png")     
    def __str__(self):
        return self.softwarecategory     

class DatabaseDetailsFields(models.Model):
    DatabaseDetails =  models.ForeignKey(DatabaseDetails, on_delete=models.CASCADE)
    fieldname = models.CharField(max_length=100)
    fieldvalue = models.CharField(max_length=100)
    def __str__(self):
        return self.fieldname

class HumanAsset(models.Model):
    organizationid  = models.IntegerField(default="0")
    summary = models.TextField()
    class Meta:
        db_table = 'HumanAsset'  
    def __str__(self):
        return 'Human Asset Summary'        

class HumanAssetEmp(models.Model):
    organizationid  = models.IntegerField(default="0")
    HumanAsset =  models.ForeignKey(HumanAsset, on_delete=models.CASCADE)
    empname = models.CharField(max_length=50)
    emp_Img = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/humanasset.jpg")     
    jobfocus  =models.CharField(max_length=50,blank=True)
    expenditure = models.DecimalField(default="0",decimal_places=2,max_digits=12,blank=True) 
    skillmap = models.CharField(max_length=100,default="",blank=True)
    skillassessmentcomments = models.CharField(max_length=200,default="",blank=True)
    alignmentscore =models.IntegerField(default="0",verbose_name ='Skill Map Analysis',blank=True)
    class Meta:
        db_table = 'HumanAssetEmp'  
    def __str__(self):
        return self.empname

class HumanAssetEmpFields(models.Model):
    HumanAssetEmp =  models.ForeignKey(HumanAssetEmp, on_delete=models.CASCADE)
    fieldname = models.CharField(max_length=100)
    fieldvalue = models.CharField(max_length=100)
    def __str__(self):
        return self.fieldname      

class BusinessContinuity(models.Model):
    organizationid  = models.IntegerField(default="0")
    summary = models.TextField()
    class Meta:
        db_table = 'BusinessContinuity'  
    def __str__(self):
        return 'Business Continuity'  

class BusinessContinuityPdf(models.Model):
    organizationid  = models.IntegerField(default="0")
    BusinessContinuity =  models.ForeignKey(BusinessContinuity, on_delete=models.CASCADE)
    pdffile = models.FileField(upload_to='dashboard/static/dashboard/doc/',blank=False)        
    uploaddate = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=100)
    class Meta:
        db_table = 'BusinessContinuitypdf'  
    def __str__(self):
        return self.title

class BusinessContinuityPdfFields(models.Model):
    BusinessContinuityPdf =  models.ForeignKey(BusinessContinuityPdf, on_delete=models.CASCADE)
    fieldname = models.CharField(max_length=100)
    fieldvalue = models.CharField(max_length=100)
    class Meta:
        db_table = 'BusinessContinuityPdfFields'  
    def __str__(self):
        return 'Business Continuity Pdf Fields'       

class IctMaturityScore(models.Model):
    organizationid  = models.IntegerField(default="0")
    parameter = models.CharField(max_length=50)
    SCORE_CHOICES = (
        ('0',0),
        ('1',1),
        ('2',2),
        ('3',3),
        ('4',4),
        ('5',5),
        ('6',6),
    )    
    score = models.CharField(max_length=2, choices=SCORE_CHOICES, default='0')     
    class Meta:
        db_table = 'IctMaturityScore'  
    def __str__(self):
        return self.parameter

class Connectivity(models.Model):
    organizationid  = models.IntegerField(default="0")
    summary = models.CharField(max_length=200)
    net_Img = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/connectivity.jpg")     
    def __str__(self):
        return 'Connectivity'

class ConnectivityFields(models.Model):
    Connectivity =  models.ForeignKey(Connectivity, on_delete=models.CASCADE)
    fieldname = models.CharField(max_length=100)
    fieldvalue = models.CharField(max_length=100)
    def __str__(self):
        return self.fieldname


class DynamicCategory(models.Model):
    organizationid  = models.IntegerField(default="0")
    categoryname = models.CharField(max_length=100)
    navigationbar = models.BooleanField(default=False)
    class Meta:
        db_table = 'dynamiccategory'  
    def __str__(self):
        return self.categoryname         


class DynamicCategoryValue(models.Model):
    DynamicCategory =  models.ForeignKey(DynamicCategory, on_delete=models.CASCADE)
    organizationid  = models.IntegerField(default="0")
    dy_Img = models.ImageField(upload_to='dashboard/static/dashboard/img/',blank=False,default="static/dashboard/img/default-img.png") 
    summary = models.CharField(max_length=200)
    class Meta:
        db_table = 'dynamiccategoryvalue'      
    def __str__(self):
        return self.DynamicCategory.categoryname       


class DynamicCategoryValueFields(models.Model):
    DynamicCategoryValue =  models.ForeignKey(DynamicCategoryValue, on_delete=models.CASCADE)
    fieldname = models.CharField(max_length=100)
    fieldvalue = models.CharField(max_length=100)
    class Meta:
        db_table = 'dynamiccategoryvaluefields'      
    def __str__(self):
        return self.fieldname    

class About(models.Model):
    summary = models.CharField(max_length=200)
    class Meta:
        db_table = 'about'  
    def __str__(self):
        return 'About'           