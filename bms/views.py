import json
from django.shortcuts import render
from bms.apps import APP_NAME
from bms.repo import CommandRepo, FeederRepo,LogRepo
from core.views import CoreContext,ParameterRepo
from bms.serializers import CommandSerializer,RelayFullSerializer, FeederSerializer, RelaySerializer,LogSerializer
from django.views import View
from utility.log import leolog
TEMPLATE_ROOT="bms/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    paramerer_repo=ParameterRepo(request=request,app_name=APP_NAME)
    SERVER_SIDE_COMMANDS=paramerer_repo.parameter(name='اجرای فرمان ها از سمت سرور',default=False).boolean_value
    CLIENT_SIDE_COMMANDS=paramerer_repo.parameter(name='اجرای فرمان ها از سمت کلاینت',default=True).boolean_value
    context['SERVER_SIDE_COMMANDS']=SERVER_SIDE_COMMANDS
    context['CLIENT_SIDE_COMMANDS']=CLIENT_SIDE_COMMANDS
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class FeedersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feeders=FeederRepo(request=request).list()
        context['feeders']=feeders
        feeders_s=json.dumps(FeederSerializer(feeders,many=True).data)
        context['feeders_s']=feeders_s
        context['expands_feeders']=True
        return render(request,TEMPLATE_ROOT+"feeders.html",context)


class CommandsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        commands=CommandRepo(request=request).list()
        context['commands']=commands
        commands_s=json.dumps(CommandSerializer(commands,many=True).data)
        context['commands_s']=commands_s
        context['expands_commands']=True
        return render(request,TEMPLATE_ROOT+"commands.html",context)


class LogView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feeders=FeederRepo(request=request).list()
        context['feeders']=feeders
        feeders_s=json.dumps(FeederSerializer(feeders,many=True).data)
        context['feeders_s']=feeders_s
        return render(request,TEMPLATE_ROOT+"log.html",context)


class LogsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        logs=LogRepo(request=request).list().order_by('-date_added')[:20]
        context['logs']=logs
        logs_s=json.dumps(LogSerializer(logs,many=True).data)
        context['logs_s']=logs_s
        return render(request,TEMPLATE_ROOT+"logs.html",context)

        
class FeederView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feeder=FeederRepo(request=request).feeder(*args, **kwargs)
        context['feeder']=feeder
        feeder_s=json.dumps(FeederSerializer(feeder).data)
        context['feeder_s']=feeder_s

        
        relays=feeder.relay_set.all().order_by('priority')
        context['relays']=relays
        relays_s=json.dumps(RelayFullSerializer(relays,many=True).data)
        context['relays_s']=relays_s

        return render(request,TEMPLATE_ROOT+"feeder.html",context)