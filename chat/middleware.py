import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'percipio.settings')  # adjust if your settings module is elsewhere

import django
django.setup()

from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
import jwt

from user.models import MyUser


@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return MyUser.objects.get(id=payload["user_id"])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, MyUser.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope["query_string"].decode())
        token_list = query_params.get("token")

        if token_list:
            token = token_list[0]
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
