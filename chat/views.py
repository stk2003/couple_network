from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def chat_room(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) |
         Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'chat/chat_room.html', {
        'receiver': receiver,
        'messages': messages
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            image=image
        )
        
        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # все пользователи кроме текущего
    return render(request, 'chat/user_list.html', {
        'users': users
    })
