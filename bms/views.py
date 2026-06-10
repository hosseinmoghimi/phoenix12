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


        commands=CommandRepo(request=request).list(for_home=True)
        context['commands']=commands
        commands_s=json.dumps(CommandSerializer(commands,many=True).data)
        context['commands_s']=commands_s
        context['expands_commands']=True

        return render(request,TEMPLATE_ROOT+"index.html",context)

class SettingsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"setting.html",context)


class GetJsonBackupView(View):
    def get(self,request,*args, **kwargs):
        from django.http import JsonResponse
        origin_feeders=FeederRepo(request=request).list()
        json_data={'feeders':[]}
        for feeder in origin_feeders:
            sss=feeder_to_json(feeder)
            json_data['feeders'].append(sss)


        return JsonResponse(json_data,safe=False)
    
def feeder_to_json(feeder):
    data={}
    data['relays']=[]
    data['id']=feeder.id
    data['name']=feeder.name
    data['ip']=feeder.ip
    data['port']=feeder.port
    data['serial_no']=feeder.serial_no
    data['color']=feeder.color
    data['pin']=feeder.pin
    data['is_protected']=feeder.is_protected
    data['thumbnail_origin']=str(feeder.thumbnail_origin)
     
 
    for relay in feeder.relay_set.all():
        data['relays'].append(relay_to_json(relay))

    return data


def relay_to_json(relay):
    data={}
    data['commands']=[]
    data['id']=relay.id
    data['name']=relay.name
    data['enabled']=relay.enabled
    data['is_protected']=relay.is_protected
    data['register']=relay.register
    data['pin']=relay.pin
    data['color']=relay.color
    data['priority']=relay.priority
    data['thumbnail_origin']=str(relay.thumbnail_origin)

 
    for command in relay.command_set.all():
        data['commands'].append(command_to_json(command))

    return data


def command_to_json(command):
    data={}
    
    data['id']=command.id
    data['name']=command.name
    data['value']=command.value
    data['color']=command.color
    data['Iteration']=command.Iteration
    data['for_home']=command.for_home
    data['persons']=[]
    data['thumbnail_origin']=str(command.thumbnail_origin)

 
    for person in command.persons.all():
        data['persons'].append(person.id)


    return data



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