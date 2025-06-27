from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PrivateChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_private_messages(request, username):
    other_user = User.objects.get(username=username)
    msgs = PrivateChatMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')
    return Response([{'from': m.sender.username, 'to': m.receiver.username, 'msg': m.message, 'time': m.timestamp} for m in msgs])
