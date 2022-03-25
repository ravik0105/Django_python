from django.contrib import admin
from django.urls import path, include
from CPSWFMS import views
from django.contrib.auth.views import LogoutView,LoginView
#from cpswfms import views
from django.views.i18n import JavaScriptCatalog
from CPSWFMS.views import EditorChartView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EditorChartView.as_view(), name='index'),
    #path('dashboard_with_pivot/', views.dashboard_with_pivot, name="dashboard_with_pivot"),
    #path('index1/',views.index1, name="index1"),
    #path('pie-chart/', views.pie_chart, name='pie-chart'),

    #path('pivot_data/', views.pivot_data, name="pivot_data"),

    path('Inventory_process/', views.Inventory_process, name="Inventory_process"),
    path('Text_process/', views.Text_process, name="Text_process"),

    #path('ce/', views.copyedit_process, name="ce"),

    path('toolprocess/', views.toolprocess, name="toolprocess"),
    path('CEReferenceprocess/', views.CEReferenceprocess, name="CEReferenceprocess"),
    path('CETextprocess/', views.CETextprocess, name="CETextprocess"),


    path('artwork/', views.art_work_process, name="artwork"),
    path('aptypesetting/', views.aptype_setting_process, name="aptypesetting"),
    path('aptypesettingqc/', views.aptype_setting_QC_process, name="aptypesettingqc"),
    #path('aptypesettingqc_corr/', views.aptype_setting_QC_Corr_process, name="aptypesettingqc_corr"),
    #path('aptypesettingqc_corr_check/', views.aptype_setting_QC_Corr_Check_process, name="aptypesettingqc_corr_check"),
    #path('std/<int:pk>', views.start_date,name='std'),
    #path('edd/<int:pk>', views.end_date,name='edd'),
#    path('edit/<int:pk>', views.edit,name='edit'),

#    path('update/<int:pk>', views.update,name='update'),
    #path('Inventory_update/<int:pk>', views.Inventory_update,name='Inventory_update'),
    #path('', views.Inventory_update,name='Inventory_update'),
    #path('update_start/<int:pk>', views.update_start,name='update_start'),
    #path('update_end/<int:pk>', views.update_end,name='update_end'),


    path('toolprocess_update_start/<int:pk>', views.toolprocess_update_start,name='toolprocess_update_start'),
    path('toolprocess_update_end/<int:pk>', views.toolprocess_update_end,name='toolprocess_update_end'),

    path('CEReferenceprocess_update_start/<int:pk>', views.CEReferenceprocess_update_start,name='CEReferenceprocess_update_start'),
    path('CEReferenceprocess_update_end/<int:pk>', views.CEReferenceprocess_update_end,name='CEReferenceprocess_update_end'),

    path('CETextprocess_update_start/<int:pk>', views.CETextprocess_update_start,name='CETextprocess_update_start'),
    path('CETextprocess_update_end/<int:pk>', views.CETextprocess_update_end,name='CETextprocess_update_end'),




    path('artwork_update/<int:pk>', views.artwork_update,name='artwork_update'),
    path('artwork_update_start/<int:pk>', views.artwork_update_start,name='artwork_update_start'),
    path('artwork_update_end/<int:pk>', views.artwork_update_end,name='artwork_update_end'),

    #path('aptype_setting_update/<int:pk>', views.aptype_setting_update,name='aptype_setting_update'),
    path('aptype_setting_update_start/<int:pk>', views.aptype_setting_update_start,name='aptype_setting_update_start'),
    path('aptype_setting_update_end/<int:pk>', views.aptype_setting_update_end,name='aptype_setting_update_end'),

#    path('aptype_setting_QC_update/<int:pk>', views.aptype_setting_QC_update,name='aptype_setting_QC_update'),
    path('aptype_setting_QC_update_start/<int:pk>', views.aptype_setting_QC_update_start,name='aptype_setting_QC_update_start'),
    path('aptype_setting_QC_update_end/<int:pk>', views.aptype_setting_QC_update_end,name='aptype_setting_QC_update_end'),

#    path('aptype_setting_QC_Corr_update/<int:pk>', views.aptype_setting_QC_Corr_update,name='aptype_setting_QC_Corr_update'),
#    path('aptype_setting_QC_Corr_Check_update/<int:pk>', views.aptype_setting_QC_Corr_Check_update,name='aptype_setting_QC_Corr_Check_update'),

    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),


#Dashboard
    path('ce-available/', views.ce_available, name="ce-available"),

    
#    path('',views.home_view,name=''),
#    path('login', LoginView.as_view(template_name='cpswfms/adminlogin.html'),name='login'),

]
