from django.shortcuts import render
from .models import Conversation , ConversationTurn

def view_conversation(request , pk):
    conversations = Conversation.objects.all().order_by('-started_at')
    
    return render(request , 'conversations/convo_list.html' , {'conversations' : conversations})


def view_conversation_detail(request , pk):
    conversation = Conversation.objects.get(pk=pk)
    turns = conversation.turns.all()

    return render(request , 'conversations/convo_detail.html' , {
        'conversation' : conversation,
        'turns' : turns
    })