from django.urls import path
from messenger import views,apis
from messenger.apps import APP_NAME
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeViews.as_view()),name="home"),
    path("channel/<int:pk>/",login_required(views.ChannelViews.as_view()),name="channel"),
    path("member/<int:pk>/",login_required(views.MemberView.as_view()),name="member"),
    
    path("send_sms/",login_required(views.SendSMSView.as_view()),name="send_sms"),
    path("message/<int:pk>/",login_required(views.MessageViews.as_view()),name="message"),
    path("send_message/",login_required(apis.SendMessageApi.as_view()),name="send_message"),
    
    path("notification/<int:pk>/",login_required(views.NotificationView.as_view()),name="notification"),
    path("notifications/<int:pk>/",login_required(views.NotificationsView.as_view()),name="notifications"),
    path("send_notification/",login_required(apis.SendNotificationApi.as_view()),name="send_notification"),
]
