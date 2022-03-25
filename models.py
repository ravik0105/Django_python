from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q


class Inventory_Upload(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    pages = models.IntegerField()
    tables = models.IntegerField()
    figures = models.IntegerField()
    math = models.BooleanField()
    r_article = models.BooleanField()
    sftp = models.BooleanField()
    L2 = models.BooleanField()
    filepath = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    received_date = models.DateField(default=timezone.now)
    query_date = models.DateField(blank=True, null=True)
    query_received_date = models.DateField(blank=True, null=True)
    FILE_ACTIVITIES = (
        ('INVE', 'Inventory'),
        ('COED', 'Copy Editing'),
        ('ARTW', 'Art Work'),
        ('AUTS', 'Author Typesetting'),
        ('ATSQ', 'Author Typesetting QC'),
        ('ATQC', 'Author Typesetting QC Correction'),
        ('AQCC', 'Author Typesetting QC Correction Check'),
        ('AURE', 'Author Review'),
        ('TREF', 'Tool and Reference Part'),
        ('TXTP', 'Text Part'),
        ('TXPU', 'Text Part User'),
    )
    activity = models.CharField(max_length=4,
    choices=FILE_ACTIVITIES,
    blank=True,
    default='INVE',
    )
    FILE_STATUS = (
        ('q', 'Query'),
        ('a', 'Available'),
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
        ('r', 'Reject'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    def __str__(self):
        #return str(self.article_id), str(self.remarks), str(self.comments)
        #return f'{self.article_id}, {self.remarks}, {self.comments}'
        return f'{self.article_id}'
class CopyEdit(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    pages = models.IntegerField()
    tables = models.IntegerField()
    figures = models.IntegerField()
    math = models.BooleanField()
    r_article = models.BooleanField()
    sftp = models.BooleanField()
    L2 = models.BooleanField()
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    FILE_ACTIVITIES = (
        ('COED', 'Copy Editing'),
        ('TREF', 'Tool and Reference Part'),
        ('TXT', 'Text Part'),
    )
    activity = models.CharField(max_length=4,
    choices=FILE_ACTIVITIES,
    blank=True,
    default='INVE',
    )
    FILE_STATUS = (
        ('q', 'Query'),
        ('a', 'Available'),
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
        ('r', 'Reject'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    def __str__(self):
        #return str(self.article_id), str(self.remarks), str(self.comments)
        #return f'{self.article_id}, {self.remarks}, {self.comments}'
        return f'{self.article_id}'

"""class CopyEdit(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date =models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.article_id)
"""

class Toolpart_Copyedit(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date =models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.article_id)

class Reference_Part(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date =models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.article_id)

class Text_Part(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date =models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.article_id)


class Text_Part_User(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date =models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.article_id)


class Art_Work(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "image_process"
    def __str__(self):
        return str(self.article_id)

class AP_Typesetting(models.Model):
    article_id = models.CharField(max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_active': True})
    #user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    image_process = models.ManyToManyField(Art_Work, limit_choices_to=Q(status='c'))
    reject_status = models.CharField(blank=True, null=True, max_length=2)
    Image_process = models.BooleanField()
    copyedit_process = models.BooleanField()
    def __str__(self):
        return str(self.article_id)

class AP_Type_QC(models.Model):
    article_id = models.CharField(max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
        ('r', 'Reject'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    reject_status = models.CharField(blank=True, null=True, max_length=2)
    Image_process = models.BooleanField()
    copyedit_process = models.BooleanField()
    def __str__(self):
        return str(self.article_id)

class AP_Type_QC_Corr(models.Model):
    article_id = models.CharField(max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    reject_status = models.CharField(blank=True, null=True, max_length=2)
    def __str__(self):
        return str(self.article_id)

class AP_Type_QC_Corr_Check(models.Model):
    article_id = models.CharField(max_length=50)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, limit_choices_to={'is_staff': True})
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
        ('r', 'Reject'),
    )
    status = models.CharField(max_length=1,
    choices=FILE_STATUS,
    blank=True,
    default='a')
    remarks = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    reject_status = models.CharField(blank=True, null=True, max_length=2)
    def __str__(self):
        return str(self.article_id)

class Author_Review(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('w', 'Working in Process'),
        ('c', 'Completed'),
        ('r', 'Reject')
    )
    status = models.CharField(max_length=1,
                              choices=FILE_STATUS
                              )
    def __str__(self):
        return str(self.article_id)

class Process_status(models.Model):
    article_id = models.CharField(max_length=50)
    user_name = models.CharField(blank=True, null=True, max_length=100)
    start_date = models.DateField(blank=True, null=True, max_length=50)
    start_time = models.TimeField(blank=True, null=True, max_length=10)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True, max_length=10)
    FILE_STATUS = (
        ('q', 'Query'),
        ('a', 'Available'),
        ('i', 'Inuse'),
        ('h', 'Hold'),
        ('c', 'Completed'),
        ('r', 'Reject'),
    )
    status = models.CharField(max_length=1,
                              choices=FILE_STATUS
                              )
    FILE_ACTIVITIES = (
        ('INVE', 'Inventory'),
        ('COED', 'Copy Editing'),
        ('ARTW', 'Art Work'),
        ('TREF', 'Tool Part'),
        ('REFP', 'Reference Part'),
        ('TXTP', 'Text Part'),
    )
    activity = models.CharField(max_length=4,
    choices=FILE_ACTIVITIES,
    blank=True,
    default='COED',
    )
    def __str__(self):
        return str(self.article_id)

class waiting_status(models.Model):
    article_id = models.CharField(unique = True, max_length=50)
    Image_process = models.BooleanField()
    Reference_process = models.BooleanField()
    Text_process = models.BooleanField()
    status = models.CharField(max_length=50)

# Create your models here.
