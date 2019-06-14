from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from .models import AccessLog,ContactCenter,Profile,FinancialAnalysisData,SocialNetwork,DatabaseDetails,\
    HumanAsset,HumanAssetEmp , BusinessContinuity,BusinessContinuityPdf,BusinessContinuityPdfFields,\
    IctMaturityScore ,Connectivity,ConnectivityFields,Organization , DynamicCategory,DynamicCategoryValue,About,SMTPDetails

# Create your views here.



def getmodulename(modulekey):
    if modulekey == 'businesscontinuity':
        return 'BUSINESS CONTINUITY'

    if modulekey == 'socialnetworks':
        return 'SOCIAL NETWORKS'

    if modulekey == 'contactcenter':
        return 'CONTACT CENTER'

    if modulekey == 'datacenter':
        return 'DATA CENTER'

    if modulekey == 'videomn':    
        return 'VIDEO MN' 

    if modulekey == 'humanassets':
        return 'HUMAN ASSETS' 

    if modulekey == 'hardware':
        return 'HARDWARE' 

    if modulekey == 'software':
        return 'SOFTWARE' 

    if modulekey == 'cloud':
        return 'CLOUD' 

    if modulekey == 'mobile':
        return 'MOBILE' 

    if modulekey == 'security':
        return 'SECURITY' 

    if modulekey == 'database':
        return 'DATABASE' 

    if modulekey == 'connectivity':   
        return 'CONNECTIIVTY' 
   

@login_required
def index(request):
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='dashboard',organizationid=profiledata.organizationid)    
    orgdata = []
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
        modulelist = str(orgdata.modules).split(',')
    except Exception as ex:
        modulelist = ['businesscontinuity','socialnetworks','contactcenter','datacenter','videomn','humanassets','hardware','software','cloud','mobile','security','database','connectivity']

    try:
        dycat = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=False)
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except Exception as ex:
        print('error ->',ex)
        dycat= []
        dycatnav =[]
        
    div_hdr = '<div class="container-fluid animatedParent animateOnce my-3"> <div class="animated fadeInUpShort"> <div class="lightSlider" data-item="3" data-item-xl="3" data-item-md="2" data-item-sm="1" data-pause="7000" data-pager="false">'
    div_ftr = '</div></div></div>'
    mlist = div_hdr
    v_cnt = 0
    for m in modulelist:
        v_cnt+=1
        mlist = mlist + '<div>' +'<a href="/'+m.replace(' ','')+'">' + '<div class="white text-center p-4">' + '<h6 class="mb-3">'+getmodulename(m.replace(' ',''))+'</h6>'+ '</div></a></div>'
        if v_cnt == 3:
            mlist = mlist + div_ftr
            mlist = mlist + div_hdr
            v_cnt = 0
    for dy in dycat:
        v_cnt+=1
        mlist = mlist + '<div>' +'<a href="/dynamiccat?id='+str(dy.id)+'">' + '<div class="white text-center p-4">' + '<h6 class="mb-3">'+dy.categoryname+'</h6>'+ '</div></a></div>'
        if v_cnt == 3:
            mlist = mlist + div_ftr
            mlist = mlist + div_hdr
            v_cnt = 0            
    mlist = mlist + div_ftr


    #print('mlist',mlist)
    return render(
        request,
        'dashboard/dashboard.html',
                {
                    'user':request.user,
                    'mlist':mlist,
                    'dycatnav':dycatnav,
                    'profiledata':profiledata,
                    'orgdata':orgdata,
                }       
    )

@login_required
def dynamiccat(request):
    assert isinstance(request, HttpRequest)
    id=request.GET.get('id','')
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='dynamiccat',organizationid=profiledata.organizationid)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []
    try:
        dcv  = DynamicCategory.objects.filter(id=id)[0]
        dcvlist  = DynamicCategoryValue.objects.filter(DynamicCategory=id)
    except:
        dcv = None
        dcvlist = None        

    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]

    return render(
        request,
        'dashboard/dynamiccat.html',
                {
                    'user':request.user ,
                    'dcvlist':dcvlist,
                    'dcname':dcv.categoryname,
                    'dycatnav':dycatnav,
                    'profiledata':profiledata,
                    'orgdata':orgdata,
                }       
    )

@login_required
def dash(request):
    assert isinstance(request, HttpRequest)
    orgdata = []
    try:
        profiledata = Profile.objects.get(user=request.user)
        aclog = AccessLog.objects.create(userid=request.user.id,pagename='dashboard',organizationid=profiledata.organizationid)
        orgdata = Organization.objects.get(id=profiledata.organizationid)
        modulelist = str(orgdata.modules).split(',')
    except Exception as ex:
        modulelist = ['businesscontinuity','socialnetworks','contactcenter','datacenter','videomn','humanassets','hardware','software','cloud','mobile','security','database','connectivity']

    try:
        dycat = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=False)
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycat= []
        dycatnav =[]
        
    div_hdr = '<div class="container-fluid animatedParent animateOnce my-3"> <div class="animated fadeInUpShort"> <div class="lightSlider" data-item="3" data-item-xl="3" data-item-md="2" data-item-sm="1" data-pause="7000" data-pager="false">'
    div_ftr = '</div></div></div>'
    mlist = div_hdr
    v_cnt = 0
    for m in modulelist:
        v_cnt+=1
        mlist = mlist + '<div>' +'<a href="/'+m.replace(' ','')+'">' + '<div class="white text-center p-4">' + '<h6 class="mb-3">'+getmodulename(m.replace(' ',''))+'</h6>'+ '</div></a></div>'
        if v_cnt == 3:
            mlist = mlist + div_ftr
            mlist = mlist + div_hdr
            v_cnt = 0
    for dy in dycat:
        v_cnt+=1
        mlist = mlist + '<div>' +'<a href="/dynamiccat?id='+str(dy.id)+'">' + '<div class="white text-center p-4">' + '<h6 class="mb-3">'+dy.categoryname+'</h6>'+ '</div></a></div>'
        if v_cnt == 3:
            mlist = mlist + div_ftr
            mlist = mlist + div_hdr
            v_cnt = 0            
    mlist = mlist + div_ftr


    #print('mlist',mlist)
    return render(
        request,
        'dashboard/dashboard.html',
                {
                    'user':request.user,
                    'mlist':mlist,
                    'dycatnav':dycatnav,
                    'profiledata':profiledata,
                    'orgdata':orgdata,
                }       
    )

@login_required
def contact(request):
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='contact',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]    
    return render(
        request,
        'dashboard/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

def about(request):
    #print(' request.is_ajax-->',request.is_ajax())
    if request.is_ajax():
        abt = About.objects.get()
        json_response = {'abt': abt.summary}
        return HttpResponse(json.dumps(json_response),content_type='application/json')

    else:
        """Renders the about page."""
        assert isinstance(request, HttpRequest)
        profiledata = Profile.objects.get(user=request.user)
        aclog = AccessLog.objects.create(userid=request.user.id,pagename='about',organizationid=profiledata.organizationid)        
        try:
            orgdata = Organization.objects.get(id=profiledata.organizationid)
        except:
            orgdata = []        
        try:
            abt = About.objects.get()
        except:
            abt =None
        try:
            dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
        except:
            dycatnav =[]           
        return render(
            request,
            'dashboard/about.html',
            {
                'title':'About',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'aboutlist':abt,
                'dycatnav':dycatnav,
                'profiledata':profiledata,
                'orgdata':orgdata,
            }
        )

@login_required
def database(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='database',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]        
    return render(
        request,
        'dashboard/database.html',
        {
            'title':'database',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dblist':DatabaseDetails.objects.filter(organizationid=profiledata.organizationid),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def connectivity(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='database',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]         
    return render(
        request,
        'dashboard/connectivity.html',
        {
            'title':'Connectivity',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'netlist':Connectivity.objects.filter(organizationid=profiledata.organizationid),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )


def in_groupname(FinancialAnalysisData, groupname):
    return FinancialAnalysisData.filter(groupname=groupname)


@login_required
def recurrentexp(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='recurrentexp',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    financialanalysisdata = FinancialAnalysisData.objects.order_by('id').filter(organizationid=profiledata.organizationid)        
    group = FinancialAnalysisData.objects.raw('SELECT *,sum(amount)as amt FROM financialanalysisdata where organizationid = {} GROUP BY groupname'.format(profiledata.organizationid))
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[] 
    context = {'group': group, 'financialanalysisdata': financialanalysisdata,'year':datetime.now().year,'dycatnav':dycatnav,'profiledata':profiledata,'orgdata':orgdata,}


    return render(request, 'dashboard/recurrentexp.html', context)
    

@login_required
def humanassets(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='humanassets',organizationid=profiledata.organizationid)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        ha = HumanAsset.objects.filter(organizationid=profiledata.organizationid)[0]
    except:
        ha = None       
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]         
    return render(
        request,
        'dashboard/humanassets.html',
        {
            'title':'HUMAN ASSETS',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ha':ha,
            'haall':None,
            'hajob':None,
            'haskill':None,
            'haexp':None,
            'haass':None,
            'alldata':None,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def gethumanassetdataall(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)    
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        ha = HumanAsset.objects.filter(organizationid=profiledata.organizationid)[0]
        hae = HumanAssetEmp.objects.filter(organizationid=profiledata.organizationid)
    except:
        ha = None    
        hae = None  
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]          
    return render(
        request,
        'dashboard/humanassets.html',
        {
            'title':'HUMAN ASSETS',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ha':ha,
            'haall':hae,
            'hajob':None,
            'haskill':None,
            'haexp':None,
            'haass':None,
            'alldata':None,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def gethumanassetdatajob(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)  
    profiledata = Profile.objects.get(user=request.user)  
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        ha = HumanAsset.objects.filter(organizationid=profiledata.organizationid)[0]
        jobgroup = HumanAssetEmp.objects.raw('SELECT *,count(*)as cnt,CEILING(avg(alignmentscore)) alignscore FROM HumanAssetEmp where organizationid ={} GROUP BY jobfocus'.format(profiledata.organizationid))
    except Exception as ex:
        print(ex)
        ha = None  
        jobgroup = None    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]         
    return render(
        request,
        'dashboard/humanassets.html',
        {
            'title':'HUMAN ASSETS',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ha':ha,
            'haall':None,
            'hajob':jobgroup,
            'haskill':None,
            'haexp':None,
            'haass':None,
            'alldata':HumanAssetEmp.objects.all(),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def gethumanassetdataskill(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)  
    profiledata = Profile.objects.get(user=request.user)   
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        ha = HumanAsset.objects.filter(organizationid=profiledata.organizationid)[0]
        jobgroup = HumanAssetEmp.objects.raw('SELECT *,CEILING(avg(alignmentscore)) alignscore FROM HumanAssetEmp where organizationid ={} GROUP BY jobfocus'.format(profiledata.organizationid))
    except Exception as ex:
        print(ex)
        ha = None  
        jobgroup = None    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]            
    return render(
        request,
        'dashboard/humanassets.html',
        {
            'title':'HUMAN ASSETS',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ha':ha,
            'haall':None,
            'hajob':None,
            'haskill':jobgroup,
            'haexp':None,
            'haass':None,
            'alldata':None,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def gethumanassetdataexp(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)    
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        ha = HumanAsset.objects.filter(organizationid=profiledata.organizationid)[0]
        jobgroup = HumanAssetEmp.objects.raw('SELECT *,count(*)as cnt,sum(expenditure) exp,CEILING(avg(alignmentscore)) alignscore FROM HumanAssetEmp where organizationid ={} GROUP BY jobfocus'.format(profiledata.organizationid))
    except:
        ha = None   
        jobgroup = None   
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]          
    return render(
        request,
        'dashboard/humanassets.html',
        {
            'title':'HUMAN ASSETS',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ha':ha,
            'haall':None,
            'hajob':None,
            'haskill':None,
            'haexp':jobgroup,
            'haass':None,
            'alldata':HumanAssetEmp.objects.all(),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )    


@login_required
def ictmaturityscore(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='ictmaturityscore',organizationid=profiledata.organizationid)
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]      
    return render(
        request,
        'dashboard/capex.html',
        {
            'title':'ICT TRENDS IN SECTOR',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ictlist':IctMaturityScore.objects.filter(organizationid=profiledata.organizationid),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def accesslogweek(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='accesslog',organizationid=profiledata.organizationid)
    try:
        acloggroup = AccessLog.objects.raw('SELECT *,count(*)as cnt FROM accessLog where datetime between  date_sub(now(),INTERVAL 1 WEEK) and now() and organizationid = {} GROUP BY pagename'.format(profiledata.organizationid))
        usrloggroup = AccessLog.objects.raw('SELECT *,username nm,count(*)as cnt FROM accessLog a , auth_user b where a.userid=b.id and datetime between  date_sub(now(),INTERVAL 1 WEEK) and now() and organizationid = {} GROUP BY userid'.format(profiledata.organizationid))
    except Exception as ex:
        print(ex)
        acloggroup = None     
        usrloggroup = None
    print('acloggroup-->',acloggroup)
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]         
    return render(
        request,
        'dashboard/accesslog.html',
        {
            'title':'ACCESS LOG',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'acloggroup':acloggroup,
            'usrloggroup':usrloggroup,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def accesslogmonth(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
   # aclog = AccessLog.objects.create(userid=request.user.id,pagename='accesslog')
    try:
        acloggroup = AccessLog.objects.raw('SELECT *,count(*)as cnt FROM accessLog where datetime between  date_sub(now(),INTERVAL 1 MONTH) and now() and organizationid = {} GROUP BY pagename'.format(profiledata.organizationid))
        usrloggroup = AccessLog.objects.raw('SELECT *,username nm,count(*)as cnt FROM accessLog a , auth_user b where a.userid=b.id and datetime between  date_sub(now(),INTERVAL 1 MONTH) and now() and organizationid = {} GROUP BY userid'.format(profiledata.organizationid))
    except:
        ha = None     
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]            
    return render(
        request,
        'dashboard/accesslog.html',
        {
            'title':'ACCESS LOG',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'acloggroup':acloggroup,
            'usrloggroup':usrloggroup,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )    

@login_required
def accesslogytd(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
   # aclog = AccessLog.objects.create(userid=request.user.id,pagename='accesslog')
    try:
        acloggroup = AccessLog.objects.raw('SELECT *,count(*)as cnt FROM accessLog where datetime between  date_sub(now(),INTERVAL 1 YEAR) and now() and organizationid = {} GROUP BY pagename'.format(profiledata.organizationid))
        usrloggroup = AccessLog.objects.raw('SELECT *,username nm,count(*)as cnt FROM accessLog a , auth_user b where a.userid=b.id and datetime between  date_sub(now(),INTERVAL 1 YEAR) and now() and organizationid = {} GROUP BY userid'.format(profiledata.organizationid))
    except:
        ha = None     
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]         
    return render(
        request,
        'dashboard/accesslog.html',
        {
            'title':'ACCESS LOG',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'acloggroup':acloggroup,
            'usrloggroup':usrloggroup,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def accesslogpytd(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
   # aclog = AccessLog.objects.create(userid=request.user.id,pagename='accesslog')
    try:
        acloggroup = AccessLog.objects.raw('SELECT *,count(*)as cnt FROM accessLog where datetime between  date_sub(now(),INTERVAL 2 YEAR) and date_sub(now(),INTERVAL 1 YEAR) and organizationid = {} GROUP BY pagename'.format(profiledata.organizationid))
        usrloggroup = AccessLog.objects.raw('SELECT *,username nm,count(*)as cnt FROM accessLog a , auth_user b where a.userid=b.id and datetime between  date_sub(now(),INTERVAL 2 YEAR) and date_sub(now(),INTERVAL 1 YEAR) and organizationid = {} GROUP BY userid'.format(profiledata.organizationid))
    except:
        ha = None     
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]          
    return render(
        request,
        'dashboard/accesslog.html',
        {
            'title':'ACCESS LOG',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'acloggroup':acloggroup,
            'usrloggroup':usrloggroup,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@csrf_exempt
def postcommentsmtp(request):
    if request.is_ajax():
        data = request.body
        jsondata  = json.loads(data)
        userlist = jsondata.get('userlist')
        toemails = []
        usrlist = User.objects.filter(id__in=userlist)
        for usr in usrlist:
            toemails.append(usr.email)

        comments = jsondata.get('comments')
        orgid = jsondata.get('orgid')
        smtpdtl = SMTPDetails.objects.get(organizationid=orgid)
        print('toemails-->',toemails)
        print('comments-->',comments)
        print('smtpdtl-->',smtpdtl)
        if len(toemails) >=1:
            backend = EmailBackend(host=smtpdtl.host, port=smtpdtl.port, username=smtpdtl.username, 
                        password=smtpdtl.passwrd, use_tls=True , fail_silently=False)    
            # backend = EmailBackend(host='smtp.gmail.com', port=587, username='sumitgpl@gmail.com', 
            #             password='sumit123#', use_tls=True , fail_silently=False)                                  

            email = EmailMessage(subject='CDASH - Post Comments message !', body=comments, from_email=smtpdtl.username, to=toemails,connection=backend)
            email.send()

    return HttpResponse(json.dumps(json_response),content_type='application/json')

@login_required
def postcomment(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    profiledata_f = Profile.objects.filter(organizationid=profiledata.organizationid)
    p_users = []
    for row in profiledata_f:
        if row.user.id != request.user.id:
            p_users.append(row.user.id)    
    usrlist = User.objects.filter(id__in=p_users)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='postcomment',organizationid=profiledata.organizationid)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]       
    return render(
        request,
        'dashboard/postcomment.html',
        {
            'title':'POST COMMENT',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'userlist':User.objects.all(),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
            'usrlist':usrlist,
        }
    )

@login_required
def socialnetworks(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='socialnetworks',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        scnet = SocialNetwork.objects.filter(organizationid=profiledata.organizationid)[0]
    except:
        scnet = None    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]             
    return render(
        request,
        'dashboard/socialnetworks.html',
        {
            'title':'SOCIAL NETWORKS',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'linklist':scnet,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )



@login_required
def businesscontinuity(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='businesscontinuity',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    #print('orgdata->',orgdata)
    try:
        bc = BusinessContinuity.objects.filter(organizationid=profiledata.organizationid)[0]
        bcpdf = BusinessContinuityPdf.objects.filter(BusinessContinuity=bc.id)
    except:
        bc = None     
        bcpdf = None   
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]           
    return render(
        request,
        'dashboard/ictmaturityscore.html',
        {
            'title':'ICT TRENDS IN SECTOR',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'bc' : bc,
            'bcpdflist': bcpdf,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )


@login_required
def contactcenter(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='contactcenter',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]      
    return render(
        request,
        'dashboard/contactcenter.html',
        {
            'title':'contact center',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'contactlist':ContactCenter.objects.filter(organizationid=profiledata.organizationid),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def datacenter(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='datacenter',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]        
    return render(
        request,
        'dashboard/datacenter.html',
        {
            'title':'data center',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def videomn(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='videomn',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]      
    return render(
        request,
        'dashboard/videomn.html',
        {
            'title':'videomn',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def hardware(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='hardware',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:    
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]      
    return render(
        request,
        'dashboard/hardware.html',
        {
            'title':'hardware',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def software(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='software',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:    
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]        
    return render(
        request,
        'dashboard/software.html',
        {
            'title':'software',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def cloud(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='cloud',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]       
    return render(
        request,
        'dashboard/cloud.html',
        {
            'title':'cloud',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def mobile(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='mobile',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]     
    return render(
        request,
        'dashboard/cloud.html',
        {
            'title':'cloud',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def security(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='security',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]     
    return render(
        request,
        'dashboard/cloud.html',
        {
            'title':'cloud',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def analytics(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='analytics',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]        
    return render(
        request,
        'dashboard/analytics.html',
        {
            'title':'analytics',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def capex(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='ictmaturityscore',organizationid=profiledata.organizationid)
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]      
    return render(
        request,
        'dashboard/capex.html',
        {
            'title':'ICT TRENDS IN SECTOR',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'ictlist':IctMaturityScore.objects.filter(organizationid=profiledata.organizationid),
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def scenarios(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='scenarios',organizationid=profiledata.organizationid)    
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]      
    return render(
        request,
        'dashboard/scenarios.html',
        {
            'title':'scenarios',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    )

@login_required
def help(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    profiledata = Profile.objects.get(user=request.user)
    aclog = AccessLog.objects.create(userid=request.user.id,pagename='help',organizationid=profiledata.organizationid)    
    try:
        dycatnav = DynamicCategory.objects.filter(organizationid=profiledata.organizationid,navigationbar=True)
    except:
        dycatnav =[]     
    try:
        orgdata = Organization.objects.get(id=profiledata.organizationid)
    except:
        orgdata = []          
    return render(
        request,
        'dashboard/help.html',
        {
            'title':'help',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'dycatnav':dycatnav,
            'profiledata':profiledata,
            'orgdata':orgdata,
        }
    ) 


