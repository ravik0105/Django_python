import sys
import urllib.request
from django.contrib import admin
from django.template import RequestContext
from .views import *
from .models import Inventory_Upload, CopyEdit, Art_Work, AP_Typesetting, AP_Type_QC, AP_Type_QC_Corr, AP_Type_QC_Corr_Check, Author_Review
#from django.utils.timezone import datetime
import datetime
from datetime import datetime
from django import forms
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
import csv, re
from django.db import connection
from .forms import *
from django.http import request, HttpResponse
from django.contrib.auth import get_user
from django.core.paginator import Paginator
# Inventory application registers
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core import serializers
from django.http import JsonResponse

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class CPSDemoAdmin(admin.ModelAdmin):
    def status_color(self, obj):
            if obj.activity == 'INVE' and not obj.status == 'q':
                return mark_safe('<b style="background:{};">{}</b>'.format('yellow', 'Open'))
            elif obj.status == 'q':
                return mark_safe('<b style="background:{};">{}</b>'.format('red', 'Query'))

            return mark_safe('<b style="background:{};">{}</b>'.format('lightgreen', 'Closed'))  # or any color for False

    list_display = ('article_id' ,'status_color', 'pages', 'tables', 'figures', 'math', 'r_article', 'sftp', 'L2', 'remarks', 'comments','activity')
    search_fields = ['article_id']
    actions = ['move_to_copyedit']
    list_per_page = 5
    def move_to_copyedit(modeladmin, request, queryset):
        queryset.update(status='a')
        queryset.update(activity='COED')
        art_list = queryset.values_list('article_id','pages','tables','figures','math','r_article','sftp','L2','remarks','comments','received_date','query_date','query_received_date','activity','status')
        for art in art_list:
#            print(art)
            a = art[0]
            p = art[1]
            t = art[2]
            f = art[3]
            m = art[4]
            if m == False:
                m = 0
            if m == True:
                m = 1
            r_a = art[5]
            if r_a == False:
                r_a = 0
            if r_a == True:
                r_a = 1
            s = art[6]
            if s == False:
                s = 0
            if s == True:
                s = 1
            l = art[7]
            if l == False:
                l = 0
            if l == True:
                l = 1
            re = art[8]
            co = art[9]
            rd = art[10]
            qd = art[11]
            qd = '0000-00-00 00:00:00'
            qrd = art[12]
            qrd = '0000-00-00 00:00:00'
            act = art[13]
            sta = art[14]
            cursor = connection.cursor()
            cursor.execute("call COPY2PROD ('"+a+"','"+str(p)+"','"+str(t)+"','"+str(f)+"','"+str(m)+"','"+str(r_a)+"','"+str(s)+"','"+str(l)+"','"+re+"','"+co+"','"+act+"','"+sta+"')")
        messages.success(request,'Object(s) is/are moved next activity')
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload-csv/', self.upload_csv),
         ]
        return new_urls + urls
        
    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            csv_data = [re.sub(r'"(.*?),(.*?)"',r'"\1cpscomma\2"',x) for x in csv_data]
            for x in csv_data:
                fields = x.split(",")
                fields = [re.sub(r'cpscomma',r',',x) for x in fields]
                fields = [re.sub(r'No',r'False',x) for x in fields]
                fields = [re.sub(r'Yes',r'True',x) for x in fields]
                fields = [re.sub(r'""$',r',',x) for x in fields]
                created = Inventory_Upload.objects.update_or_create(
                    article_id = fields[0],
                    pages = fields[1],
                    tables = fields[2],
                    figures = fields[3],
                    math = fields[4],
                    r_article = fields[5],
                    sftp = fields[6],
                    L2 = fields[7],
                    filepath = fields[8],
                    remarks = fields[9],
                    comments = fields[10],
                )
            messages.warning(request, 'Upload completed...')
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {'form': form}
        return render(request, "admin/csv_upload.html", data)

class CPSCopyEditAdmin(admin.ModelAdmin):
#    list_display = ('article_id','colored_first_name',)
    def status_color(self, obj):
            if obj.activity == 'COED' and not obj.status == 'q':
                return mark_safe('<b style="background:{};">{}</b>'.format('yellow', 'Open'))
            elif obj.status == 'q':
                return mark_safe('<b style="background:{};">{}</b>'.format('red', 'Query'))

            return mark_safe('<b style="background:{};">{}</b>'.format('lightgreen', 'Closed'))  # or any color for False


    list_display = ('article_id', 'status_color', 'pages', 'tables', 'figures', 'math', 'r_article', 'sftp', 'L2', 'remarks', 'comments', 'activity', 'status')
    search_fields = ['article_id']
    actions = ['assign_to_user']
    list_per_page = 8

#    date_hierarchy = 'added_on'
    def assign_to_user(modeladmin, request, queryset):
        users = User.objects.filter(groups__name='ToolProcess')
        art_list = queryset.values_list('article_id','remarks','comments')
        for art in art_list:
            a = art[0]
            r = art[1]
            c = art[2]
            s = 'TREF'
            cursor = connection.cursor()
            cursor.execute("call COPY2PROD_CE ('"+a+"','"+r+"','"+c+"')")
            cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
        messages.success(request,'Object(s) is/are moved next activity')
        querysets = str(queryset)
        with open("copyedit_in.txt", 'w', encoding='utf-8') as output:
            output.write(querysets)
        return render(request, "admin/broadcast_message.html", {'items': queryset, 'users': users})

    def Inventory_process(self, request):
        articles = CMODEL.Inventory_Upload.objects.all()
        users = User.objects.filter(groups__name='ToolProcess')
        return render(request, 'cpswfms/inventory_process.html',{'articles':articles, 'users':users})
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('results/', self.Inventory_process),
        ]
        return new_urls + urls

# CPS Tool Admin

class CPSToolAdmin(admin.ModelAdmin):
    list_display = ('article_id','status')
    def toolprocess(self, request):
        articles = CMODEL.Toolpart_Copyedit.objects.all()
        return render(request, 'cpswfms/toolprocess.html',{'articles':articles})

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
            form.data._mutable=True
            user = request.user
            articles.start_date = d
            articles.start_time = t
            articles.user_name = user
            form.save()
            return redirect('toolprocess')
        return render(request, 'cpswfms/toolprocess_update_start.html',{'articles':articles,'form':form})

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
#            print(a)
#            print(r)
#            print(c)
#            print(s)
            cursor = connection.cursor()
            cursor.execute("call COPY2PROD_CE ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
            cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
        #messages.success(request,'Object(s) is/are moved next activity')
            messages.success(request,'Object(s) is/are moved next activity')
            form.save()
#            print(form)
            return redirect('toolprocess')
        return render(request, 'cpswfms/toolprocess_update_end.html',{'articles':articles,'form':form})

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
        path('toolprocess/', toolprocess, name="toolprocess"),
        path('toolprocess_update_start/<int:pk>', toolprocess_update_start,name='toolprocess_update_start'),
        path('toolprocess_update_end/<int:pk>', toolprocess_update_end,name='toolprocess_update_end'),
        ]
        return new_urls + urls
class CPSReferenceAdmin(admin.ModelAdmin):
    list_display = ('article_id','status')
    # remove default delete actions
    def CEReferenceprocess(self, request):
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
            form.data._mutable=True
            user = request.user
            articles.start_date = d
            articles.start_time = t
            articles.user_name = user
            #form.data._mutable=False
    #       print(form)
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
            print(a)
            print(r)
            print(c)
            print(s)
#            cursor = connection.cursor()
#            cursor.execute("call COPY2PROD_CE ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
#            cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
        #messages.success(request,'Object(s) is/are moved next activity')
#            messages.success(request,'Object(s) is/are moved next activity')
            form.save()
            print(form)
            return redirect('CEReferenceprocess')
        return render(request, 'cpswfms/CEReferenceprocess_update_end.html',{'articles':articles,'form':form})


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
        path('CEReferenceprocess/', CEReferenceprocess, name="CEReferenceprocess"),
        path('CEReferenceprocess_update_start/<int:pk>', CEReferenceprocess_update_start,name='CEReferenceprocess_update_start'),
        path('CEReferenceprocess_update_end/<int:pk>', CEReferenceprocess_update_end,name='CEReferenceprocess_update_end'),
        ]
        return new_urls + urls

class CPSTextAdmin(admin.ModelAdmin):

    def status_color(self, obj):
            if obj.status == '':
                return mark_safe('<b style="background:{};">{}</b>'.format('yellow', 'Open'))
            elif obj.status == 'q':
                return mark_safe('<b style="background:{};">{}</b>'.format('red', 'Query'))

            return mark_safe('<b style="background:{};">{}</b>'.format('lightgreen', 'Closed'))  # or any color for False
    list_per_page = 5
    list_display = ('article_id','status_color','status')
    search_fields = ['article_id']
    actions = ['assign_to_user1']
    # remove default delete actions
    def assign_to_user1(modeladmin, request, queryset):
        users = User.objects.filter(groups__name='TextTeam')
        art_list = queryset.values_list('article_id','remarks','comments')
        for art in art_list:
            a = art[0]
            r = art[1]
            c = art[2]
            s = 'TXPU'
            cursor = connection.cursor()
            cursor.execute("call COPY2PROD_CE1 ('"+a+"','"+r+"','"+c+"')")
            cursor.execute("call COPY2PROD_CE1_ST ('"+a+"','"+s+"')")
        messages.success(request,'Object(s) is/are moved next activity')
        querysets = str(queryset)
        with open("textprocess_in.txt", 'w', encoding='utf-8') as output:
            output.write(querysets)
        return render(request, "admin/Textprocess_message.html", {'items': queryset, 'users': users})

    def Text_process(self, request):
        articles = CMODEL.Text_Part.objects.all()
        users = User.objects.filter(groups__name='TextTeam')
        return render(request, 'cpswfms/Text_process.html',{'articles':articles, 'users':users})
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('results1/', self.Text_process),
        ]
        return new_urls + urls

class CPSTextUserAdmin(admin.ModelAdmin):
    list_display = ('article_id','status')
    # remove default delete actions
#    def text_user_process(self, request):
    def CETextprocess(request):
        articles = CMODEL.Text_Part_User.objects.all()
        return render(request, 'cpswfms/CETextprocess.html',{'articles':articles})

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
            form.save()
            return redirect('CETextprocess')
        return render(request, 'cpswfms/CETextprocess_update_start.html',{'articles':articles,'form':form})

        # Edit Forms End button
    def CETextprocess_update_end(request, pk):
        articles = CMODEL.Text_Part_User.objects.all()
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
            cursor = connection.cursor()
            cursor.execute("call COPY2PROD_CE ('"+a+"','"+r+"','"+c+"')") # duplicate entry update arrested
            cursor.execute("call COPY2PROD_CE_ST ('"+a+"','"+s+"')")
            messages.success(request,'Object(s) is/are moved next activity')
            form.save()
            print(form)
            return redirect('CETextprocess')
        return render(request, 'cpswfms/CETextprocess_update_end.html',{'articles':articles,'form':form})

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('CETextprocess/', CETextprocess, name="CETextprocess"),
            path('CETextprocess_update_start/<int:pk>', CETextprocess_update_start,name='CETextprocess_update_start'),
            path('CETextprocess_update_end/<int:pk>', CETextprocess_update_end,name='CETextprocess_update_start'),
        ]
        return new_urls + urls

class CPSArtworkAdmin(admin.ModelAdmin):
    list_display = ('article_id','status')
    # remove default delete actions
    def art_work_process(self, request):
        articles = CMODEL.Art_Work.objects.all()
        return render(request, 'cpswfms/artwork_process.html',{'articles':articles})

    def artwork_update(request, pk):
        articles = CMODEL.Art_Work.objects.get(id=pk)
        form = ArtworkForm(request.POST or None, instance=articles)
        if form.is_valid():
            form.save()
            return redirect('artwork')
        return render(request, 'cpswfms/artwork_update.html',{'articles':articles,'form':form})


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('artwork/', art_work_process, name="artwork"),
            path('artwork_update/<int:pk>', artwork_update,name='artwork_update'),
        ]
        return new_urls + urls



class CPS_AP_Typeset_Admin(admin.ModelAdmin):
    list_display = ('article_id','status')
    # remove default delete actions
    actions = ['move_to_next_activity']

    def aptype_setting_process(self, request):
        articles = CMODEL.AP_Typesetting.objects.all()
        return render(request, 'cpswfms/aptype_setting_process.html',{'articles':articles})


    def aptype_setting_update(request, pk):
        articles = CMODEL.AP_Typesetting.objects.get(id=pk)
        form = APTypesettingForm(request.POST or None, instance=articles)
        if form.is_valid():
            form.save()
            return redirect('aptypesetting')
        return render(request, 'cpswfms/aptype_setting_update.html',{'articles':articles,'form':form})

    def aptype_setting_update_start(request, pk):
        articles = CMODEL.AP_Typesetting.objects.get(id=pk)
        form = APTypesettingForm(request.POST or None, instance=articles)
        if form.is_valid():
            d = datetime.today()
            t = datetime.now()
            print(d)
            print(t)
            form.save()
            return redirect('aptypesetting')
        return render(request, 'cpswfms/aptype_setting_update_start.html',{'articles':articles,'form':form})

    def aptype_setting_update_end(request, pk):
        articles = CMODEL.AP_Typesetting.objects.get(id=pk)
        form = APTypesettingForm(request.POST or None, instance=articles)
        if form.is_valid():
            form.save()
            return redirect('aptypesetting')
        return render(request, 'cpswfms/aptype_setting_update_end.html',{'articles':articles,'form':form})



    def move_to_next_activity(modeladmin, request, queryset):
        art_list = queryset.values_list('article_id','remarks','comments','reject_status')
        for art in art_list:
            print(art)
            a = art[0]
            r = art[1]
            c = art[2]
            r_s = art[3]
            #aa = art[0]
            s = 'ATSQ'
            if r_s == None:
                r_s = 'C1'
            cursor = connection.cursor()
            cursor.execute("call APTSP_NA ('"+a+"','"+r+"','"+c+"','"+r_s+"')")
            cursor.execute("call COPY2PROD_APT_UP ('"+a+"','"+s+"')")
        messages.success(request,'Object(s) is/are moved next activity')

            #cursor.execute("call COPY2PROD_APT_UP ('"+a+"','"+s+"')")
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('aptypesetting/', aptype_setting_process, name="aptypesetting"),
            path('aptype_setting_update/<int:pk>', aptype_setting_update,name='aptype_setting_update'),
        ]
        return new_urls + urls

class CPS_AP_Typeset_QC_Admin(admin.ModelAdmin):
    list_display = ('article_id','status')
    actions = ['move_to_next_activity']

    def aptype_setting_QC_process(self, request):
        articles = CMODEL.AP_Type_QC.objects.all()
        return render(request, 'cpswfms/aptype_setting_QC_process.html',{'articles':articles})

    def aptype_setting_QC_update(request, pk):
        articles = CMODEL.AP_Type_QC.objects.get(id=pk)
        form = APTypesettingQCForm(request.POST or None, instance=articles)
        if form.is_valid():
            form.save()
            return redirect('aptypesettingqc')
        return render(request, 'cpswfms/aptype_setting_QC_update.html',{'articles':articles,'form':form})

    def move_to_next_activity(modeladmin, request, queryset):
        art_list = queryset.values_list('article_id','remarks','comments','status','reject_status')
        for art in art_list:
            print(art)
            a = art[0]
            r = art[1]
            c = art[2]
            s = art[3]
            r_s = art[4]
            if r_s=='C1':
                r_s = 'C2'
            elif r_s=='C2':
                r_s = 'C3'
            elif r_s=='C3':
                r_s = 'C4'
            elif r_s == 'C4':
                r_s = 'C5'
            aa = art[0]
            p_aure = 'AURE'
            p_atqc = 'AUTS'
            cursor = connection.cursor()
            cursor.execute("call APTSQC_CORR_CHECK ('"+s+"','"+a+"','"+r+"','"+c+"','"+r_s+"')")
            cursor.execute("call APTSQC_CORR_CHECK_UP ('"+s+"','"+p_aure+"','"+p_atqc+"','"+a+"')")
        messages.success(request,'Object(s) is/are moved next activity')
    # remove default delete actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('aptypesettingqc/', aptype_setting_QC_process, name="aptypesettingqc"),
            path('aptype_setting_QC_update/<int:pk>', aptype_setting_QC_update,name='aptype_setting_QC_update'),
        ]
        return new_urls + urls


class CPS_AP_Typeset_QC_Corr_Admin(admin.ModelAdmin):
    list_display = ('article_id','status')
    actions = ['move_to_next_activity']

    def aptype_setting_QC_Corr_process(self, request):
        articles = CMODEL.AP_Type_QC_Corr.objects.all()
        return render(request, 'cpswfms/aptype_setting_QC_Corr_process.html',{'articles':articles})

    def aptype_setting_QC_Corr_update(request, pk):
        articles = CMODEL.AP_Type_QC_Corr.objects.get(id=pk)
        form = APTypesettingQCCorrForm(request.POST or None, instance=articles)
        if form.is_valid():
            form.save()
            return redirect('aptypesettingqc_corr')
        return render(request, 'cpswfms/aptype_setting_QC_Corr_update.html',{'articles':articles,'form':form})

# Need to update strored procedure for done and reject
    def move_to_next_activity(modeladmin, request, queryset):
        art_list = queryset.values_list('article_id','remarks','comments','reject_status')
        for art in art_list:
            print(art)
            a = art[0]
            r = art[1]
            c = art[2]
            r_s = art[3]
            aa = art[0]
            aqcc = 'AQCC'
            if r_s == None:
                r_s = 'C1'
            print("a",a)
            print("r",r)
            print("c",c)
            print("r_s",r_s)
            print("aa", aa)
            print("aqcc", aqcc)
            cursor = connection.cursor()
            cursor.execute("call APTSQC_CORR_NP ('"+a+"','"+r+"','"+c+"','"+r_s+"')")
            cursor.execute("call APTSQC_CORR_NP_UP ('"+aqcc+"','"+aa+"')")
        messages.success(request,'Object(s) is/are moved next activity')
    # remove default delete actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('aptypesettingqc_corr/', aptype_setting_QC_Corr_process, name="aptypesettingqc_corr"),
            path('aptype_setting_QC_Corr_update/<int:pk>', aptype_setting_QC_Corr_update,name='aptype_setting_QC_Corr_update'),
        ]
        return new_urls + urls


class CPS_AP_Typeset_QC_Corr_QC_Admin(admin.ModelAdmin):
    list_display = ('article_id','status')
    actions = ['move_to_next_activity']

    def aptype_setting_QC_Corr_Check_process(self, request):
        articles = CMODEL.AP_Type_QC_Corr_Check.objects.all()
        return render(request, 'cpswfms/aptype_setting_QC_Corr_Check_process.html',{'articles':articles})

    def aptype_setting_QC_Corr_Check_update(request, pk):
        articles = CMODEL.AP_Type_QC_Corr_Check.objects.get(id=pk)
        form = APTypesettingQCCorrCheckForm(request.POST or None, instance=articles)
        if form.is_valid():
            form.save()
            return redirect('aptypesettingqc_corr_check')
        return render(request, 'cpswfms/aptype_setting_QC_Corr_Check_update.html',{'articles':articles,'form':form})

# Need to update strored procedure for done and reject
    def move_to_next_activity(modeladmin, request, queryset):
        art_list = queryset.values_list('article_id','remarks','comments','status','reject_status')
        for art in art_list:
            print(art)
            a = art[0]
            r = art[1]
            c = art[2]
            s = art[3]
            r_s = art[4]
            if r_s=='C1':
                r_s = 'C2'
            elif r_s=='C2':
                r_s = 'C3'
            elif r_s=='C3':
                r_s = 'C4'
            elif r_s == 'C4':
                r_s = 'C5'
            aa = art[0]
            p_aure = 'AURE'
            p_atqc = 'ATQC'
            cursor = connection.cursor()
            cursor.execute("call APTSQC_CORR_CHECK ('"+s+"','"+a+"','"+r+"','"+c+"','"+r_s+"')")
            cursor.execute("call APTSQC_CORR_CHECK_UP ('"+s+"','"+p_aure+"','"+p_atqc+"','"+a+"')")
            
        messages.success(request,'Object(s) is/are moved next activity')
    # remove default delete actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('aptypesettingqc_corr_check/', aptype_setting_QC_Corr_Check_process, name="aptypesettingqc_corr_check"),
            path('aptype_setting_QC_Corr_Check_update/<int:pk>', aptype_setting_QC_Corr_Check_update,name='aptype_setting_QC_Corr_Check_update'),
        ]
        return new_urls + urls


class CPS_Author_Review_Admin(admin.ModelAdmin):
    list_display = ('article_id','status')
    # remove default delete actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Inventory_Upload, CPSDemoAdmin)
admin.site.register(CopyEdit, CPSCopyEditAdmin)
admin.site.register(Toolpart_Copyedit, CPSToolAdmin)
admin.site.register(Reference_Part, CPSReferenceAdmin)
admin.site.register(Text_Part, CPSTextAdmin)
admin.site.register(Text_Part_User, CPSTextUserAdmin)
admin.site.register(Art_Work, CPSArtworkAdmin)
admin.site.register(AP_Typesetting, CPS_AP_Typeset_Admin)
admin.site.register(AP_Type_QC, CPS_AP_Typeset_QC_Admin)

#admin.site.register(AP_Type_QC_Corr, CPS_AP_Typeset_QC_Corr_Admin)
#admin.site.register(AP_Type_QC_Corr_Check, CPS_AP_Typeset_QC_Corr_QC_Admin)
admin.site.register(Author_Review, CPS_Author_Review_Admin)
# Register your models here.
