from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.http import JsonResponse

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

# Create your views here.
from .models import Room
from django.contrib.auth.models import User
import logging

logger = logging.getLogger()

@login_required
def all_rooms(request):
    rooms = request.user.room_set.all()
    context = {'rooms': rooms, 'user': request.user}
    if request.GET.get('username'):
        results =  User.objects.filter(username__contains=request.GET.get('username'))
        if len(results) == 0:
            context['error_message'] = 'No users matched your search criteria. '
        else:
            context['profiles'] = results
    return render(request, 'chat/index.html', context)

@login_required
def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})

@login_required
def token(request):
    identity = request.GET.get('identity', request.user.username)
    device_id = request.GET.get('device', 'default')  # unique device ID
    
    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        # 'token': token.to_jwt().decode('utf-8')
        'token': token.to_jwt()
    }

    return JsonResponse(response)