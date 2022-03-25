from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.test import tag
from . forms import ArtworkForm, CopyeditForm, APTypesettingForm, APTypesettingQCForm, APTypesettingQCCorrForm, APTypesettingQCCorrCheckForm, CEToolForm, CEReferenceForm, CETextForm, CETextUserForm
from . import models as CMODEL
from django.contrib import messages
from django.db import connection
from django.utils.timezone import datetime
from django.utils import timezone
from datetime import datetime, time, date
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from .models import Art_Work, CopyEdit, Reference_Part, Toolpart_Copyedit, Text_Part, Text_Part_User, Process_status
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
import re
from DemoProject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import get_connection
from django.core import serializers
from django.http import JsonResponse
from django.views.generic import TemplateView
#from django.db.models import Sum
from collections import Counter
from django.db.models import Count

class EditorChartView(TemplateView):
    template_name = 'CPSWFMS/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["articles"] = CMODEL.Process_status.objects.all()
        context["articles"] = CMODEL.Process_status.objects.all()
        context["dataset"] = CMODEL.Process_status.objects.values('activity').annotate(count=Count('id')).order_by()
        context["process_status"] = CMODEL.Process_status.objects.values('status','activity').annotate(count=Count('id')).order_by()
        return context


today = datetime.today()

# Create your views here.

# Inventory Views
def Inventory_process(request):
    articles = CMODEL.Inventory_Upload.objects.all()
    #articles = CMODEL.Inventory_Upload.objects.filter(activity__name='COED')
    results = request.GET['names']
    with open("copyedit_user.txt", 'w', encoding='utf-8') as output:
        output.write(results)
    
    with open("copyedit_in.txt", 'r', encoding='utf-8') as input:
        with open("copyedit_out.txt", 'w') as output:
            for line in input:
                line = re.sub(r'<CopyEdit: ', r'', line)
                line = re.sub(r'<QuerySet \[', r'', line)
                line = re.sub(r'>', r'', line)
                line = re.sub(r'\]', r'', line)
                output.write(line)
    u = open("copyedit_user.txt", 'r')
    user_name_to_assign = u.readline()
    print(user_name_to_assign)
    user_name = User.objects.get(username=user_name_to_assign).pk
    email = User.objects.get(username=user_name_to_assign).email
    print(user_name)
    f = open("copyedit_out.txt", 'r')
    a = f.readline()
    artlist = a.replace(r',','\n')
    subject = 'Tool and Reference objects for processsing...'
    message = 'Hi %s,\n\n Please find the objects list for Tool and Reference process.\n\nArticle List:\n----------------\n %s\n\nRegards,\nCopyedit Team\n' % (str(user_name_to_assign), str(artlist))
    print(message)
    recepient = str(email)
    print(recepient)
    print(EMAIL_HOST_USER)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

    i = a.split(", ")
    for art in i:
        cursor = connection.cursor()
        cursor.execute("call TR_user_update ('"+art+"','"+str(user_name)+"')")
    return render(request, 'cpswfms/inventory_process.html',{'articles':articles, 'names':results})
def Text_process(request):
    articles = CMODEL.Text_Part.objects.all()
    results = request.GET['names']
    with open("text_user.txt", 'w', encoding='utf-8') as output:
        output.write(results)
    with open("textprocess_in.txt", 'r', encoding='utf-8') as input:
        with open("textprocess_out.txt", 'w') as output:
            for line in input:
                line = re.sub(r'<Text_Part: ', r'', line)
                line = re.sub(r'<QuerySet \[', r'', line)
                line = re.sub(r'>', r'', line)
                line = re.sub(r'\]', r'', line)
                output.write(line)
    u = open("text_user.txt", 'r')
    user_name_to_assign = u.readline()
    print(user_name_to_assign)
    user_name = User.objects.get(username=user_name_to_assign).pk
    email = User.objects.get(username=user_name_to_assign).email
    print(user_name)
    f = open("textprocess_out.txt", 'r')
    a = f.readline()
    artlist = a.replace(r',','\n')
    subject = 'Text Process objects for processsing...'
    message = 'Hi %s,\n\n Please find the objects list for Text process.\n\nArticle List:\n----------------\n %s\n\nRegards,\nCopyedit Team\n' % (str(user_name_to_assign), str(artlist))
    print(message)
    recepient = str(email)
    print(recepient)
    print(EMAIL_HOST_USER)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

    i = a.split(", ")
    for art in i:
        cursor = connection.cursor()
        cursor.execute("call TXTPro_user_update ('"+art+"','"+str(user_name)+"')")
    return render(request, 'cpswfms/text_process.html',{'articles':articles, 'names':results})

# Tool Part
def toolprocess(request):
    articles = CMODEL.Toolpart_Copyedit.objects.all()
    get_user_id = request.user
    f_get_user_id = get_user_id.id
    return render(request, 'cpswfms/toolprocess.html',{'get_user_id':f_get_user_id, 'articles':articles})

def toolprocess_update_start(request, pk):
    articles = CMODEL.Toolpart_Copyedit.objects.get(id=pk)
    form = CEToolForm(request.POST or None, instance=articles)
    if form.is_valid():
        if articles.status=='':
            articles.status = 'i'
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        a = articles.article_id
        form.data._mutable=True
        user = request.user
        articles.start_date = d
        articles.start_time = t
        articles.user_name = user
        s = 'i'
        u = str(user)
        cursor = connection.cursor()
        cursor.execute("call TOOLPROCESS_START ('"+a+"','"+str(d)+"','"+str(t)+"','"+s+"','"+u+"')")
        form.save()
        return redirect('toolprocess')
    return render(request, 'cpswfms/toolprocess_update_start.html',{'articles':articles, 'form':form})

    # Edit Forms End button
def toolprocess_update_end(request, pk):
    articles = CMODEL.Toolpart_Copyedit.objects.get(id=pk)
    form = CEToolForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.end_date = d
        articles.end_time = t
        articles.user_name = user
        a = articles.article_id
        r = articles.remarks
        c = articles.comments
        s = 'TREF'
        user_name = User.objects.get(username=user).pk
        print(user_name)
        st = articles.status
        cursor = connection.cursor()
        cursor.execute("call TOOLPROCESS_NA ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
        cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
        cursor.execute("call TOOLPROCESS_ST ('"+a+"','"+str(user_name)+"')")
        cursor.execute("call TOOLPROCESS_END ('"+a+"','"+str(d)+"','"+str(t)+"','"+st+"')")
        messages.success(request,'Object(s) is/are moved next activity')
        form.save()
        print(form)
        return redirect('toolprocess')
    return render(request, 'cpswfms/toolprocess_update_end.html',{'articles':articles,'form':form})

# Reference Part
def CEReferenceprocess(request):
    articles = CMODEL.Reference_Part.objects.all()
    get_user_id = request.user
    f_get_user_id = get_user_id.id
    return render(request, 'cpswfms/CEReferenceprocess.html',{'get_user_id':f_get_user_id, 'articles':articles})

def CEReferenceprocess_update_start(request, pk):
    articles = CMODEL.Reference_Part.objects.get(id=pk)
    form = CEReferenceForm(request.POST or None, instance=articles)
    if form.is_valid():
        if articles.status=='':
            articles.status = 'i'
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        a = articles.article_id
        form.data._mutable=True
        user = request.user
        articles.start_date = d
        articles.start_time = t
        articles.user_name = user
        s = 'i'
        u = str(user)
        cursor = connection.cursor()
        cursor.execute("call CEREFERENCEPART_START ('"+a+"','"+str(d)+"','"+str(t)+"','"+s+"','"+u+"')")

        form.save()
        return redirect('CEReferenceprocess')
    return render(request, 'cpswfms/CEReferenceprocess_update_start.html',{'articles':articles,'form':form})

    # Edit Forms End button
def CEReferenceprocess_update_end(request, pk):
    articles = CMODEL.Reference_Part.objects.get(id=pk)
    form = CEReferenceForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.end_date = d
        articles.end_time = t
        articles.user_name = user
        a = articles.article_id
        r = articles.remarks
        c = articles.comments
        s = 'AUTS'
        r_p = '1'
        st = articles.status
        cursor = connection.cursor()
        cursor.execute("call CEREFERENCEPART_END ('"+a+"','"+str(d)+"','"+str(t)+"','"+st+"')")
        cursor.execute("call CEREFERENCEPART_END_NA ('"+a+"','"+r_p+"')")

#        cursor = connection.cursor()
#        cursor.execute("call COPY2PROD_CE ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
#        cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
    #messages.success(request,'Object(s) is/are moved next activity')
#        messages.success(request,'Object(s) is/are moved next activity')
        form.save()
        print(form)
        return redirect('CEReferenceprocess')
    return render(request, 'cpswfms/CEReferenceprocess_update_end.html',{'articles':articles,'form':form})


# Text Part
def CETextprocess(request):
    get_user_id = request.user
    f_get_user_id = get_user_id.id
    articles = CMODEL.Text_Part_User.objects.all()
    return render(request, 'cpswfms/CETextprocess.html',{'get_user_id':f_get_user_id, 'articles':articles})

def CETextprocess_update_start(request, pk):
    articles = CMODEL.Text_Part_User.objects.get(id=pk)
    form = CETextUserForm(request.POST or None, instance=articles)
    if form.is_valid():
        if articles.status=='':
            articles.status = 'i'
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.start_date = d
        articles.start_time = t
        articles.user_name = user
        a = articles.article_id
        s = 'i'
        u = str(user)
        cursor = connection.cursor()
        cursor.execute("call TEXTPROCESS_START ('"+a+"','"+str(d)+"','"+str(t)+"','"+s+"','"+u+"')")

        form.save()
        return redirect('CETextprocess')
    return render(request, 'cpswfms/CETextprocess_update_start.html',{'articles':articles,'form':form})

    # Edit Forms End button
def CETextprocess_update_end(request, pk):
    articles = CMODEL.Text_Part_User.objects.get(id=pk)
    form = CETextUserForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.end_date = d
        articles.end_time = t
        articles.user_name = user
        a = articles.article_id
        r = articles.remarks
        c = articles.comments
        s = 'AUTS'
        r_p = '1'
        st = articles.status
        cursor = connection.cursor()
        cursor.execute("call TEXTPROCESS_END ('"+a+"','"+str(d)+"','"+str(t)+"','"+st+"')")
        cursor.execute("call TEXTPROCESS_END_NA ('"+a+"','"+r_p+"')")

#        cursor.execute("call COPY2PROD_CE ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
#        cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
        messages.success(request,'Object(s) is/are moved next activity')
        form.save()
        print(form)
        return redirect('CETextprocess')
    return render(request, 'cpswfms/CETextprocess_update_end.html',{'articles':articles,'form':form})


# Art work
def art_work_process(request):
    articles = CMODEL.Art_Work.objects.all()
    return render(request, 'cpswfms/artwork_process.html',{'articles':articles})

def artwork_update(request, pk):
    articles = CMODEL.Art_Work.objects.get(id=pk)
    form = ArtworkForm(request.POST or None, instance=articles)
    if form.is_valid():
        form.save()
        return redirect('artwork')
    return render(request, 'cpswfms/artwork_update.html',{'articles':articles,'form':form})

def artwork_update_start(request, pk):
    articles = CMODEL.Art_Work.objects.get(id=pk)
    form = ArtworkForm(request.POST or None, instance=articles)
    if form.is_valid():
        if articles.status=='':
            articles.status = 'i'
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.start_date = d
        articles.start_time = t
        articles.user_name = user
        a = articles.article_id
        s = 'i'
        u = str(user)
        cursor = connection.cursor()
        cursor.execute("call IMAGEPROCESS_START ('"+a+"','"+str(d)+"','"+str(t)+"','"+s+"','"+u+"')")
        form.save()
        return redirect('artwork')
    return render(request, 'cpswfms/artwork_update_start.html',{'articles':articles,'form':form})

    # Edit Forms End button
def artwork_update_end(request, pk):
    articles = CMODEL.Art_Work.objects.get(id=pk)
    form = ArtworkForm(request.POST or None, instance=articles)
    if form.is_valid():
        if articles.status== '---------':
            articles.status== 'i'
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.end_date = d
        articles.end_time = t
        articles.user_name = user
        a = articles.article_id
        r = articles.remarks
        c = articles.comments
        s = 'AUTS'
        st = articles.status
        r_p = '1'

        cursor = connection.cursor()
#        cursor.execute("call Artwork ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
#        cursor.execute("call ArtWork_UP ('"+a+"','"+s+"')")
        cursor.execute("call IMAGEPROCESS_END ('"+a+"','"+str(d)+"','"+str(t)+"','"+st+"')")
        cursor.execute("call IMAGEPROCESS_END_NA ('"+a+"','"+r_p+"')")
        form.save()
        print(form)
        return redirect('artwork')
    return render(request, 'cpswfms/artwork_update_end.html',{'articles':articles,'form':form})


# AP typesetting

def aptype_setting_process(request):
    articles = CMODEL.AP_Typesetting.objects.all()
    return render(request, 'cpswfms/aptype_setting_process.html',{'articles':articles})

    # OLD Add Form Start button Not in use
def aptype_setting_update(request, pk):
    articles = CMODEL.AP_Typesetting.objects.get(id=pk)
    form = APTypesettingForm(request.POST or None, instance=articles)
    if form.is_valid():
        print(form)
        form.save()
        return redirect('aptypesetting')
    return render(request, 'cpswfms/aptype_setting_update.html',{'articles':articles,'form':form})

    # Add Forms start button
def aptype_setting_update_start(request, pk):
    articles = CMODEL.AP_Typesetting.objects.get(id=pk)
    form = APTypesettingForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.start_date = d
        articles.start_time = t
        articles.user_name = user
        print(form)
        form.save()
        return redirect('aptypesetting')
    return render(request, 'cpswfms/aptype_setting_update_start.html',{'articles':articles,'form':form})


    # Edit Forms End button
def aptype_setting_update_end(request, pk):
    articles = CMODEL.AP_Typesetting.objects.get(id=pk)
    form = APTypesettingForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.end_date = d
        articles.end_time = t
        articles.user_name = user

        aa = articles.article_id
        ar = articles.remarks
        ac = articles.comments
        r_s = articles.reject_status
        i_p = articles.Image_process
        c_p = articles.copyedit_process
        if i_p == True:
            i_p = 1
        if i_p == False:
            i_p = 0

        if c_p == True:
            c_p = 1
        if c_p == False:
            c_p = 0

        #aa = art[0]
        s = 'ATSQ'
        if r_s == None:
            r_s = 'C1'
        cursor = connection.cursor()
        cursor.execute("call APTSP_NA ('"+aa+"','"+ar+"','"+ac+"','"+r_s+"','"+str(i_p)+"', '"+str(c_p)+"')") # working here....................
        cursor.execute("call COPY2PROD_APT_UP ('"+aa+"','"+s+"')")
        form.save()
        #messages.success(request,'Object(s) is/are moved next activity')
        return redirect('aptypesetting')
    return render(request, 'cpswfms/aptype_setting_update_end.html',{'articles':articles,'form':form})
    #messages.success(request,'Object(s) is/are moved next activity')

# AP typesetting QC
def aptype_setting_QC_process(request):
    articles = CMODEL.AP_Type_QC.objects.all()
    return render(request, 'cpswfms/aptype_setting_QC_process.html',{'articles':articles})

def aptype_setting_QC_update(request, pk):
    articles = CMODEL.AP_Type_QC.objects.get(id=pk)
    form = APTypesettingQCForm(request.POST or None, instance=articles)
    if form.is_valid():
        form.save()
        return redirect('aptypesettingqc')
    return render(request, 'cpswfms/aptype_setting_QC_update.html',{'articles':articles,'form':form})

def aptype_setting_QC_update_start(request, pk):
    articles = CMODEL.AP_Type_QC.objects.get(id=pk)
    form = APTypesettingQCForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.start_date = d
        articles.start_time = t
        articles.user_name = user
        form.save()
        return redirect('aptypesettingqc')
    return render(request, 'cpswfms/aptype_setting_QC_update_start.html',{'articles':articles,'form':form})

def aptype_setting_QC_update_end(request, pk):
    articles = CMODEL.AP_Type_QC.objects.get(id=pk)
    form = APTypesettingQCForm(request.POST or None, instance=articles)
    if form.is_valid():
        now = datetime.now()
        today = datetime.today()
        d = today
        t = now
        form.data._mutable=True
        user = request.user
        articles.end_date = d
        articles.end_time = t
        articles.user_name = user
        a = articles.article_id
        r = articles.remarks
        c = articles.comments
        s = articles.status

        i_p = articles.Image_process
        c_p = articles.copyedit_process
        if i_p == True:
            i_p = 1
        if i_p == False:
            i_p = 0

        if c_p == True:
            c_p = 1
        if c_p == False:
            c_p = 0
        r_s = articles.reject_status
        if r_s=='C1':
            r_s = 'C2'
        elif r_s=='C2':
            r_s = 'C3'
        elif r_s=='C3':
            r_s = 'C4'
        elif r_s == 'C4':
            r_s = 'C5'
        aa = articles.article_id
        p_aure = 'AURE'
        p_atqc = 'ATQC'
        cursor = connection.cursor()
        cursor.execute("call APTSQC_CORR_CHECK ('"+s+"','"+a+"','"+r+"','"+c+"','"+r_s+"','"+str(i_p)+"', '"+str(c_p)+"')")#,'"+str(i_p)+"', '"+str(c_p)+"'
        cursor.execute("call APTSQC_CORR_CHECK_UP ('"+s+"','"+p_aure+"','"+p_atqc+"','"+a+"')")
        form.save()
        return redirect('aptypesettingqc')
    return render(request, 'cpswfms/aptype_setting_QC_update_end.html',{'articles':articles,'form':form})



def ce_available(request):
    articles = CMODEL.Process_status.objects.all()
    return render(request, 'cpswfms/available.html',{'articles':articles})
    