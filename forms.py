from collections import UserList
from email.policy import default
from django import forms
from django.contrib.auth.models import User
from .models import Inventory_Upload, CopyEdit, Art_Work, AP_Typesetting, AP_Type_QC, AP_Type_QC_Corr, AP_Type_QC_Corr_Check, Author_Review, Toolpart_Copyedit, Reference_Part, Text_Part, Text_Part_User
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

from django.contrib.admin import widgets

class InventoryForm(forms.ModelForm):
#    article_id = forms.CharField(disabled=True)
    class Meta:
        model=Inventory_Upload
        fields=['article_id','pages','tables','figures','math','r_article','sftp','L2','activity']

class CopyeditForm(forms.ModelForm):
    #articles=forms.ModelChoiceField(queryset=CopyEdit.objects.all())
    #print(articles)
    article_id = forms.CharField(disabled=True)
    #status = MultipleChoiceFilter(choices=MY_CHOICES, null_label='Any', null_value='')


    class Meta:
        model=CopyEdit
        #status = forms.ChoiceField(choices=(('a','Available'),('i','Inuse','c','Completed')))

        #model=Inventory_Upload
        fields=['article_id','status','remarks','comments']
        #'start_date': forms.TimePickerInput(),
        #widgets = {
        #start_date = forms.DateField(label="Starting date", widget=AdminDateWidget(attrs={'start_date': 'date'}))
        
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }
        #exclude = ('status',)

class CEToolForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=Toolpart_Copyedit
        fields=['article_id','status','remarks','comments']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }

class CEReferenceForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=Reference_Part
        fields=['article_id','status','remarks','comments']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }

class CETextForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=Text_Part
        fields=['article_id','status','remarks','comments']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }

class CETextUserForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=Text_Part_User
        fields=['article_id','status','remarks','comments']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }


class ArtworkForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=Art_Work
        fields=['article_id','status','remarks','comments']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }
        

class APTypesettingForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    """article_id = forms.CharField(required=True),
    start_date = forms.DateField(required=True),
    start_time = forms.TimeField(required=True),
    end_date = forms.DateField(required=True),
    end_time = forms.TimeField(required=True),
    status = forms.ChoiceField(required=True),
    remarks = forms.Textarea(),
    comments = forms.Textarea(),
    user_name = forms.CharField(required=True),
    image_process = forms.BooleanField(),
    reject_status = forms.CharField(),"""
    class Meta:
        model=AP_Typesetting
        #fields=['article_id','start_date','start_time','end_date','end_time','status','remarks','comments','user_name','image_process','reject_status']
        fields=['article_id','status','remarks','comments','reject_status','Image_process','copyedit_process']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }
        
class APTypesettingQCForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=AP_Type_QC
        fields=['article_id','status','remarks','comments','reject_status']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }
class APTypesettingQCCorrForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=AP_Type_QC_Corr
        fields=['article_id','status','remarks','comments','reject_status']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }
class APTypesettingQCCorrCheckForm(forms.ModelForm):
    article_id = forms.CharField(disabled=True)
    class Meta:
        model=AP_Type_QC_Corr_Check
        fields=['article_id','status','remarks','comments','reject_status']
        widgets = {
        "start_date":  AdminDateWidget(),
        "start_time":  AdminTimeWidget(),
        "end_date":  AdminDateWidget(),
        "end_time":  AdminTimeWidget(),
        }
class AllotedForm(forms.Form):
    _selected_article = forms.CharField(widget=forms.MultipleHiddenInput)
#class AllotedForm1(forms.Form):
#    _selected_article = forms.CharField(widget=forms.MultipleHiddenInput)
    
#class ExampleForm(forms.Form):
#    c = User.objects.filter(groups__name='Copyedit')
#    choices = forms.ChoiceField(widget = forms.RadioSelect(choices=c))
            #attrs = {'class' : 'form-check-input'}
        
    
    
