from django.shortcuts import render,redirect,reverse
from core.views import CoreContext
from django.views import View
from .repo import LogRepo
from log.apps import APP_NAME
TEMPLATE_ROOT="log/"
LAYOUT_PARENT="phoenix/layout.html"
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context



class IndexView(View):
    def get(self,request,*args, **kwargs):
        # context=getContext(request=request)
        # return render(request,TEMPLATE_ROOT+"index.html",context)
        return redirect(reverse(APP_NAME+":logs"))
        # return LogsView().get(request=request)
class LogView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        log=LogRepo(request=request).log(*args, **kwargs)
        context['log']=log
        return render(request,TEMPLATE_ROOT+"log.html",context)
class LogsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        logs=LogRepo(request=request).list(*args, **kwargs).order_by("-date_added")
        context['logs']=logs
        context['expand_logs']=True
        return render(request,TEMPLATE_ROOT+"logs.html",context)