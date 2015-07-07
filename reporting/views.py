from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import CrashReport
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.db import connection
from django.contrib.auth.decorators import login_required
import json
import logging
import ast
import re


@csrf_exempt
def report_android(request):
    DEBUG = True
    SESSION_NAME = "app_session"

    if(request.method=="PUT" or request.method=="POST"):
        #log.log(logging.DEBUG, "got put "+ str(request.body) )
        json_data = json.loads(request.body.decode('utf-8'))
        description = "";
        if "description" in json_data:
            description = json_data["description"]
        
        DEBUG = json_data['APP_VERSION_CODE'] == 10509999
        if DEBUG:
            log.log(logging.DEBUG, "REQUEST:: %s"%json_data['APP_VERSION_CODE'])
                
        
        notallow = ["description","solved",SESSION_NAME]
        crashreport= CrashReport()
        for key in json_data.keys():
            #if (DEBUG):
            #   log.log(logging.DEBUG, "Key: %s in POST" % (key) )
            if(not key.lower() in notallow):
                if(getattr(crashreport,key.lower(),None)!=None):
                    #if(DEBUG):
                    #   log.log(logging.DEBUG, "ADDING %s -> %s" % (key.lower(),json_data[key]) )
                    v = getattr(crashreport,key.lower(),None)
                    if(v!=None):
                        setattr(crashreport,key.lower(),json_data[key])
        crashreport.save()
    
    return HttpResponse(json.dumps({"ok":"true"}), content_type="application/json")


@login_required
def index(request):
    packages = CrashReport.objects.order_by().values('package_name').distinct()
    print(packages)
    return render(request, 'reporting/index.html', {
        "packages": packages
        })

@login_required
def package(request, package):
    if 'toggle-solved' in request.GET and 'status' in request.GET:
        reports = request.GET['toggle-solved'].split(',')

        for r in reports:
            if len(r) > 0:
                report = CrashReport.objects.filter(package_name=package, id=r).first()
                report.solved = 'solved' if (request.GET['status'] == 'False') else 'unsolved'
                report.save()

        return redirect('/reports/android/%s/' % (report.package_name))            

    unique = {}
    reports = CrashReport.objects.filter(package_name=package).order_by('-created')

    for r in reports:
        x = re.sub(r'\.java:([0-9]+)\)\n', 'REMOVED', r.stack_trace)
        if x in unique:
            if r.app_version_name in unique[x]['reports']:
                unique[x]['reports'][r.app_version_name].append(r)
            else:
                unique[x]['reports'][r.app_version_name] = [r]

            unique[x]['solved'] = unique[x]['solved'] and r.solved == 'solved'
            
            unique[x]['count'] = unique[x]['count'] + 1
            if r.created > unique[x]['last_reported']:
                unique[x]['last_reported'] = r.created
        else:
            unique[x] = {
                'reports': {r.app_version_name: [r]},
                'count': 1,
                'solved': r.solved == 'solved',
            }

            unique[x]['last_reported'] = r.created

            unique[x]['short'] = re.compile('\n\tat').split(r.stack_trace)[0]

    l = []

    for u in unique:
        l.append(unique[u])

    s = sorted(l, key=lambda k: k['last_reported'], reverse=True)
    return render(request, 'reporting/package.html', {
        "unique": s,
        "package": package,
        "reports": reports
        })

def try_literal_eval(x):
    try:
        return ast.literal_eval(x)
    except:
        return {}

@login_required
def report(request, package, id):
    report = CrashReport.objects.filter(package_name=package, id=id).first()

    if 'toggle-solved' in request.GET:
        if report.solved == 'solved':
            report.solved = 'unsolved'
        else:
            report.solved = 'solved'

        report.save()
        return redirect('/reports/android/%s/%d/' % (report.package_name, report.id))

    if 'description' in request.POST:
        report.description = request.POST['description']
        report.save()

        report = CrashReport.objects.filter(package_name=package, id=id).first()

    return render(request, 'reporting/report.html', {
        "package": package,
        "report": report,
        "logcat": report.logcat.split('\n'),
        "environment": try_literal_eval(report.environment),
        "shared_preferences": try_literal_eval(report.shared_preferences),
        "initial_configuration": try_literal_eval(report.initial_configuration),
        "crash_configuration": try_literal_eval(report.crash_configuration),
        "device_build": try_literal_eval(report.build),
        "device_display": try_literal_eval(report.display),
        "device_settings_global": try_literal_eval(report.settings_global),
        "device_settings_system": try_literal_eval(report.settings_system),
        "device_settings_secure": try_literal_eval(report.settings_secure),
        "device_features": try_literal_eval(report.device_features),
        })
