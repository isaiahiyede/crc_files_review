from django.db import models
from institutions.models import Institution
from institutions.customstorage import SFTPStorage
from django.core.files.storage import FileSystemStorage
import os
from os import sep
from django.conf import settings
from datetime import datetime
from django.core.exceptions import ValidationError
from accounts.models import MyUser
from functools import partial
from django.db.models.signals import pre_save
from storages.backends.sftpstorage import SFTPStorage

# Create your models here.
SFS = SFTPStorage()
private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)


def date_vars():
    return datetime.now().strftime('%Y'), datetime.now().strftime('%m%B'), datetime.now().strftime('%d%a')


def get_user_institution(instance, filename):
    return MyUser.objects.get(id=instance.user.id).first().userprofile.institution.short_name


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.csv', '.xls', '.xlsx', '.txt', '.zip', '.rar', '.docx', '.doc']
    if not ext.lower() in valid_extension:
        raise ValidationError(u'Error: Unsupported File Upload! Please upload txt, csv, xls, zip or rar files only.')


def fix_file_path(sender, instance, *args, **kwargs):

    if instance.submission_type == 'divs':
        instance.file.field.upload_to = os.path.join(instance.file.field.upload_to,"DIV/" + 
                                                    instance.user.userprofile.institution.short_name)
    elif instance.submission_type == 'cir':
        instance.file.field.upload_to = os.path.join(instance.file.field.upload_to,"CIR/" +
                                                     instance.user.userprofile.institution.short_name)
    elif instance.submission_type == 'update':
        instance.file.field.upload_to = os.path.join(instance.file.field.upload_to,"UPDATES/" +
                                                     instance.user.userprofile.institution.short_name)

def get_upload_to(instance, filename):
    if instance.submission_type == 'cir':
        return 'upload/%d/%s' % (instance.userprofile, instance.user.userprofile.institution.short_name)


def get_upload_file(instance, filename):
    inst_name = instance.user.userprofile.institution.short_name
    dpid = instance.user.userprofile.institution.sb2id
    submission_date = datetime.strftime(datetime.now(), "%d-%m-%Y")
    original_name = filename.split('.')[0]
    ext = filename.split('.')[-1]
    filename = f"{original_name}___{inst_name}-{dpid}-{submission_date}.{ext}"
    if instance.submission_type == 'cir':
        directory = f"{date_vars()[0]}/{date_vars()[1]}/CIR/Submitted On {date_vars()[2]}/{inst_name}"
    elif instance.submission_type == 'divs':
        directory = directory = f"{date_vars()[0]}/{date_vars()[1]}/DIVS/Submitted On {date_vars()[2]}/{inst_name}"
    elif instance.submission_type == 'update':
        directory = directory = f"{date_vars()[0]}/{date_vars()[1]}/UPDATES/Submitted On {date_vars()[2]}/{inst_name}"
    else:
        directory = directory = f"{date_vars()[0]}/{date_vars()[1]}/API/Submitted On {date_vars()[2]}/{inst_name}"
    if not os.path.exists(directory):
       os.makedirs(directory)
    full_path = str(directory)+"/%s" %(filename)
    return full_path


class UploadLog(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='uploader', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    institution_id = models.CharField(max_length=200, blank=True)
    file_name = models.CharField(max_length=200, blank=True)
    submission_type = models.CharField(max_length=40, blank=True, null=True)
    crc_admin = models.CharField(max_length=50, blank=True, null=True)
    inst_admin = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    inst_pk = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, max_length=50, blank=True, null=True)
    file = models.FileField(
        upload_to=get_upload_file,
        max_length=500,
        blank=False,
        validators=[validate_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'UploadLog'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return '%s' %(self.file_name)


class APIFiles(models.Model):
    user_short_name = models.CharField(max_length=200, blank=True, null=True)
    file_name = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(storage=private_storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'APIFiles'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return '%s' %(self.file_name)


class Documents(models.Model):
    """ save files here """
    institution_name = models.CharField(max_length=200, blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_field = models.FileField(upload_to="file_downlods", blank=True, null=True, max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    report_obj = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return '%s' %(self.file_name)