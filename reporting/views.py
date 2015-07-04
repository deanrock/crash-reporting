from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import CrashReport
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.db import connection
from django.contrib.auth.decorators import login_required
import json
import logging


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
