from django.shortcuts import render, HttpResponse, redirect
from submissions.forms import FileUploadForm, createDocForm
from submissions.models import UploadLog, Documents
from django.contrib.auth import update_session_auth_hash
from accounts.models import MyUser, UserProfile, DataManager
import os
import requests
from os import sep
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import get_template, render_to_string
import csv
import paramiko
from tempfile import mkstemp
import sys
import sqlite3
import pysftp
from institutions.models import Action, Institution
import pandas as pd
from django.db.models import Q
from submissions.tasks import *
import json
from django.http import HttpResponse
import socket

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
# from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import UploadLog
from .serializers import UploadLogSerializer


def get_ip_address(request):
    hostname = socket.gethostname()    
    ip = socket.gethostbyname(hostname)    
    return ip


def checkCategory(value):
    result = "COMMERCIAL BANKS/OTHERS"
    val = value[:4]
    if val == "2ABL":
        result = "MICRO LENDERS"
    elif val == "2A4L":
        result = "MORTGAGE"
    else:
        result = result
    return result


@api_view(['GET'])
def file_uploads(request,date_obj):
    getFiles.delay(date_obj)
    return True


@login_required
def update_file(request):
    context = {}
    ip = get_ip_address(request)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES or None)
        print(request.POST, request.FILES)
        req_obj = request.user
        # print(form)
        if form.is_valid():

            upld = form.save(commit=False)
            upld.user_id = req_obj.id
            upld.description = form.cleaned_data['description']
            upld.file = form.cleaned_data['file']
            upld.file_name = upld.file.name
            upld.institution_id = req_obj.userprofile.institution_id
            upld.save()

            get_user_inst = Institution.objects.get(sb2id=req_obj.userprofile.institution_id)
            get_user_inst.uploaded_file = True
            user_inst_name = str(get_user_inst.name)

            get_upload = UploadLog.objects.get(pk=upld.pk)
            get_upload.crc_admin = req_obj.userprofile.crcadmin

            if req_obj.userprofile.role_id == 1:
                get_upload.inst_admin = req_obj.username
            else:
                get_upload.inst_admin = req_obj.userprofile.inst_admin
            get_upload.created_by = req_obj.username
            get_upload.inst_pk = get_user_inst
            get_upload.save()

            userInst = req_obj.userprofile.institution.short_name
            filePath = upld.file.path
            print(filePath)

            submission_type = request.POST.get('submission_type')
            print(f"submission type is {submission_type.upper()}")

            user_name = req_obj.userprofile.first_name

            sftp_connection.delay(str(submission_type).upper(), str(filePath), str(upld.file), str(request.FILES.get('file')), userInst,
                             user_name)
            
            act, ip = 'Uploaded a new update file to the portal', ip
            aut = user_name + ' ' + req_obj.userprofile.last_name
            action = Action(
                action=act, 
                ip=ip, user=aut, 
                username=req_obj.email,
                crcadmin=req_obj.userprofile.crcadmin,
                instadmin=req_obj.userprofile.inst_admin)
            action.save()

            notify_crc_update.delay(upld.description, upld.file_name, user_name, user_inst_name)
            notify_uploader_update.delay(upld.description, upld.file_name, user_name, req_obj.email)
            context['success'] = "The file was uploaded successfully"
            context['form'] = FileUploadForm()
            return render(request, 'submissions/update_file.html', context)
        else:
            print(form.errors)
            context['rp'] = request.POST
            context['error'] = form.errors
            context['form'] = FileUploadForm()
            if request.user.userprofile.role.designation == "Super Admin" or request.user.userprofile.role.designation == "CRC Support Staff":
                return render(request, 'submissions/update_file.html', context)
            else:
                return render(request, 'submissions/update_file.html', context)
    else:
        context['form'] = FileUploadForm()
        if request.user.userprofile.role.designation == "Super Admin" or request.user.userprofile.role.designation == "CRC Support Staff":
            template_name = 'submissions/update_file.html'
            return render(request, template_name, context)
        else:
            template_name = 'submissions/update_file.html'
            return render(request, template_name, context)


@login_required
def upload(request):
    context = {}
    ip = get_ip_address(request)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES or None)
        print(request.POST, request.FILES)
        req_obj = request.user
        # print(form)
        if form.is_valid():

            upld = form.save(commit=False)
            upld.user_id = req_obj.id
            upld.description = form.cleaned_data['description']
            upld.file = form.cleaned_data['file']
            upld.file_name = upld.file.name
            upld.institution_id = req_obj.userprofile.institution_id
            upld.save()

            get_user_inst = Institution.objects.get(sb2id=req_obj.userprofile.institution_id)
            get_user_inst.uploaded_file = True
            user_inst_name = str(get_user_inst.name)

            get_upload = UploadLog.objects.get(pk=upld.pk)
            get_upload.crc_admin = req_obj.userprofile.crcadmin

            if req_obj.userprofile.role_id == 1:
                get_upload.inst_admin = req_obj.username
            else:
                get_upload.inst_admin = req_obj.userprofile.inst_admin
            get_upload.created_by = req_obj.username
            get_upload.inst_pk = get_user_inst
            get_upload.save()

            userInst = req_obj.userprofile.institution.short_name
            filePath = upld.file.path
            print(filePath)

            submission_type = request.POST.get('submission_type')
            print(f"submission type is {submission_type.upper()}")

            user_name = req_obj.userprofile.first_name

            sftp_connection.delay(str(submission_type).upper(), str(filePath), str(upld.file), str(request.FILES.get('file')), userInst,
                             user_name)
            
            act, ip = 'Uploaded a new file to the portal', ip
            aut = user_name + ' ' + req_obj.userprofile.last_name
            action = Action(
                action=act, 
                ip=ip, user=aut, 
                username=req_obj.email,
                crcadmin=req_obj.userprofile.crcadmin,
                instadmin=req_obj.userprofile.inst_admin)
            action.save()

            notify_crc.delay(upld.description, upld.file_name, user_name, user_inst_name)
            notify_uploader.delay(upld.description, upld.file_name, user_name, req_obj.email)
            context['success'] = "The file was uploaded successfully"
            context['form'] = FileUploadForm()
            return render(request, 'submissions/adminUpload_file.html', context)
        else:
            print(form.errors)
            context['rp'] = request.POST
            context['error'] = form.errors
            context['form'] = FileUploadForm()
            if request.user.userprofile.role.designation == "Super Admin" or request.user.userprofile.role.designation == "CRC Support Staff":
                return render(request, 'submissions/adminUpload_file.html', context)
            else:
                return render(request, 'submissions/upload_file.html', context)
    else:
        context['form'] = FileUploadForm()
        if request.user.userprofile.role.designation == "Super Admin" or request.user.userprofile.role.designation == "CRC Support Staff":
            template_name = 'submissions/adminUpload_file.html'
            return render(request, template_name, context)
        else:
            template_name = 'submissions/upload_file.html'
            return render(request, template_name, context)


@login_required
def all_uploads(request):
    if request.user.userprofile.role.designation == "Super Admin" or request.user.userprofile.role.designation == "CRC Support Staff":
        files = UploadLog.objects.all().values("inst_pk__name","description","submission_type",
            "user__userprofile__first_name","user__userprofile__last_name","user__userprofile__role__designation","uploaded_at")
        total = files.count()
        template_name = 'submissions/uploads.html'
    else:
        request.user.userprofile.role.designation == "Standard User" or request.user.userprofile.role.designation == "Institution Admin"
        user_inst_id = str(request.user.userprofile.institution).split(" ")[-1]
        files = UploadLog.objects.filter(institution_id=user_inst_id).values("inst_pk__name","description","submission_type",
            "user__userprofile__first_name","user__userprofile__last_name","user__userprofile__role__designation","uploaded_at")
        total = files.count()
        template_name = 'submissions/uploads.html'
    args = {'files': files}
    return render(request, template_name, args)


@login_required
def create_doc(request):
    context = {}
    context['item'] = 'all_docs_creations'
    context['subitem'] = 'all_docs_creations'
    context['institutions'] = Institution.objects.values('sb2id','name').exclude(status=0)
    template_name = 'submissions/create_doc.html'
    if request.method == 'POST':
        rp = request.POST
        form = createDocForm(request.POST,request.FILES)
        if form.is_valid():
            context['success'] = "File was successfully uploaded"
            form.save()
            inst_obj = Institution.objects.get(name = rp.get('institution_name'))
            emails = inst_obj.general_email, "datasubmission@crccreditbureau.com"
            notify_user_new_doc.delay(rp.get('file_name'), rp.get('institution_name'), emails)
            ip = get_ip_address(request)
            act = request.user.username + ' created a document for ' + rp.get('institution_name') 
            aut = "{} {}".format(request.user.userprofile.first_name,request.user.userprofile.last_name)
            action = Action.objects.create(action=act, ip=ip, user=aut, username=request.user.email) 
        else:
            print(form.errors)
            context['rp'] = rp
            context['error'] = form.errors
            return render(request, template_name, context)
    return render(request, template_name, context)


@login_required
def download_file(request):
    context = {}
    context['item'] = 'all_docs_downloads'
    context['subitem'] = 'all_docs_downloads'
    all_docs = []
    all_documents = Documents.objects.filter(institution_name=request.user.userprofile.institution.name)
    for doc in all_documents:
        if not doc.file_field:
            pass
        else:
            all_docs += [doc]
    context['all_docs'] = all_docs
    template_name = 'submissions/doc_downloads.html'
    return render(request, template_name, context)

