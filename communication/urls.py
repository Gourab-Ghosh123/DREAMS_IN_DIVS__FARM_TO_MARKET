from django.urls import path
from . import views
from . import views_website

urlpatterns = [
    # the sms or call trigger....
    path('api/triger/' , views.webhook_trigger , name = 'trigger'),

    # Twilio calls this....
    path('api/call/conversation/' , views.conversation_handler , name='conversation'),

    path('conversations/', views.view_conversations , name='conversations'),
    path('conversations/<int:pk>/', views.view_conversation_detail , name='conversation_detail'),

]