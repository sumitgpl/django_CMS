from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

# Register your models here.

from .models import Organization, ContactCenter, FinancialAnalysisData ,\
    Profile,SocialNetwork,DatabaseDetails,ContactCenterFields,DatabaseDetailsFields, \
    HumanAsset,HumanAssetEmp,HumanAssetEmpFields ,\
    BusinessContinuity,BusinessContinuityPdf,BusinessContinuityPdfFields ,\
    IctMaturityScore,Connectivity,ConnectivityFields,SMTPDetails,\
    DynamicCategory, DynamicCategoryValue , DynamicCategoryValueFields,About


class MyUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if request.user.username != 'superadmin':
            perm_fields = ('is_active', 'is_staff',
                            'groups')
        else:
            perm_fields = ('is_active', 'is_staff',
                            'groups', 'user_permissions')    
                                
        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]
    def get_queryset(self, request):
        query = super(MyUserAdmin, self).get_queryset(request)
        if request.user.username=='superadmin':
            return query
        else:
            profiledata = Profile.objects.get(user=request.user)
            profiledata_f = Profile.objects.filter(organizationid=profiledata.organizationid)
            p_users = []
            for row in profiledata_f:
                p_users.append(row.user.id)
            #print('p_users-->',p_users)
            filtered_query = query.filter(id__in=p_users)
            return filtered_query    

    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.save()
        try:
            profileexits = Profile.objects.get(user_id=obj.id)
        except:
            Profile.objects.create(user_id=obj.id,organizationid=profiledata.organizationid)
              

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)                

class OrgAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if request.user.username != 'superadmin':
            perm_fields = ('orgname', 'org_Img',
                            'summary')   
        else:
            perm_fields = ('orgname', 'org_Img',
                            'summary','user','modules')   

        return [(None, {'fields': perm_fields})]    

    def get_queryset(self, request):
        query = super(OrgAdmin, self).get_queryset(request)
        if request.user.username=='superadmin':
            return query
        else:        
            profiledata = Profile.objects.get(user=request.user)
            filtered_query = query.filter(id=profiledata.organizationid)
            return filtered_query 


admin.site.register(Organization,OrgAdmin)

class ProfileAdmin(admin.ModelAdmin):
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(ProfileAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query
    # def get_changeform_initial_data(self, request):
    #     profiledata = Profile.objects.get(user=request.user)
    #     print('profiledata->',profiledata)
    #     return {'organizationid': profiledata.organizationid}

admin.site.register(Profile,ProfileAdmin)
#admin.site.register(Profile)

class FinancialAnalysisDataAdmin(admin.ModelAdmin):
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(FinancialAnalysisDataAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query
      

admin.site.register(FinancialAnalysisData,FinancialAnalysisDataAdmin)

class SocialNetworkAdmin(admin.ModelAdmin):
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(SocialNetworkAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query
    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'socialnetworks' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True          

admin.site.register(SocialNetwork,SocialNetworkAdmin)

class IctMaturityScoreAdmin(admin.ModelAdmin):
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(IctMaturityScoreAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query

admin.site.register(IctMaturityScore,IctMaturityScoreAdmin)


class ContactCenterFieldsInline(admin.TabularInline):
    model = ContactCenterFields

class ContactCenterAdmin(admin.ModelAdmin):
    inlines = [
        ContactCenterFieldsInline,
    ]

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        
    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'contactcenter' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def get_queryset(self, request):
        query = super(ContactCenterAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query    

admin.site.register(ContactCenter,ContactCenterAdmin)

class DatabaseDetailsFieldsInline(admin.TabularInline):
    model = DatabaseDetailsFields

class DatabaseDetailsAdmin(admin.ModelAdmin):
    inlines = [
        DatabaseDetailsFieldsInline,
    ]

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(DatabaseDetailsAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query    
    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'database' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True   


admin.site.register(DatabaseDetails,DatabaseDetailsAdmin)

class HumanAssetAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = HumanAsset.objects.all().count()
        if count == 0:
            return True
        return False

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(HumanAssetAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query     

    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'humanassets' in str(modulelist):
                    print('true')
                    return True
                else:
                    print('false')
                    return False
            else:
                return True
        else:
            return True           

admin.site.register(HumanAsset,HumanAssetAdmin)

class HumanAssetEmpFieldsInline(admin.TabularInline):
    model = HumanAssetEmpFields

class HumanAssetEmpAdmin(admin.ModelAdmin):
    inlines = [
        HumanAssetEmpFieldsInline,
    ]

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(HumanAssetEmpAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query        

    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'humanassets' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True             

admin.site.register(HumanAssetEmp,HumanAssetEmpAdmin)


class BusinessContinuityAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = BusinessContinuity.objects.all().count()
        if count == 0:
            return True
        return False

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(BusinessContinuityAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query       

    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'businesscontinuity' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True                 

admin.site.register(BusinessContinuity,BusinessContinuityAdmin)

class BusinessContinuityPdfFieldsInline(admin.TabularInline):
    model = BusinessContinuityPdfFields

class BusinessContinuityPdfAdmin(admin.ModelAdmin):
    inlines = [
        BusinessContinuityPdfFieldsInline,
    ]
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(BusinessContinuityPdfAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query    
    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'businesscontinuity' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True       

admin.site.register(BusinessContinuityPdf,BusinessContinuityPdfAdmin)


class ConnectivityFieldsInline(admin.TabularInline):
    model = ConnectivityFields

class ConnectivityAdmin(admin.ModelAdmin):
    inlines = [
        ConnectivityFieldsInline,
    ]

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(ConnectivityAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query      

    def has_module_permission(self, request):
        if request.user.is_authenticated == True:
            if request.user.username != 'superadmin':
                profiledata = Profile.objects.get(user=request.user)
                orgdata = Organization.objects.get(id=profiledata.organizationid)
                modulelist = str(orgdata.modules).split(',')
                if 'connectivity' in str(modulelist):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True         

admin.site.register(Connectivity,ConnectivityAdmin)

class smtpAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = SMTPDetails.objects.all().count()
        if count == 0:
            return True
        return False
        
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(smtpAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query              

admin.site.register(SMTPDetails,smtpAdmin)        

class DynamicCategoryAdmin(admin.ModelAdmin):

    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(DynamicCategoryAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query   

admin.site.register(DynamicCategory,DynamicCategoryAdmin)

class DynamicCategoryValueFieldsInline(admin.TabularInline):
    model = DynamicCategoryValueFields

class DynamicCategoryValueAdmin(admin.ModelAdmin):
    inlines = [
        DynamicCategoryValueFieldsInline,
    ]
    exclude=("organizationid",)
    readonly_fields=('organizationid', )
    def save_model(self, request, obj, form, change):
        profiledata = Profile.objects.get(user=request.user)
        #print('profiledata->',profiledata)
        obj.organizationid = profiledata.organizationid
        obj.save()        

    def get_queryset(self, request):
        query = super(DynamicCategoryValueAdmin, self).get_queryset(request)
        profiledata = Profile.objects.get(user=request.user)
        filtered_query = query.filter(organizationid=profiledata.organizationid)
        return filtered_query       

admin.site.register(DynamicCategoryValue,DynamicCategoryValueAdmin)


class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = About.objects.all().count()
        if count == 0:
            return True
        return False         

admin.site.register(About,AboutAdmin)  