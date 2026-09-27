# users/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from .models import UserOnlineStatus
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

CustomUser = get_user_model()


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get('query_string', b'').decode()
        token_key = None
        
        # Парсим query параметры
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                if key == 'token':
                    token_key = value
                    break
        
        user = None
        if token_key:
            user = await self.get_user_from_token(token_key)
        
        if user:
            await self.accept()
            self.user = user
            self.user_group_name = f"user_{user.id}"
            
            # Добавляем пользователя в его персональную группу
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            
            # Обновляем статус онлайн
            await self.update_user_status(user.id, True)
            
            # Получаем список онлайн пользователей
            online_users = await self.get_online_users_data()
            
            # Отправляем информацию о подключении
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'Connected!',
                'user_id': str(user.id),
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'online_users': online_users
            }))
            
            # Уведомляем всех о новом онлайн пользователе
            await self.channel_layer.group_send(
                "online_users",
                {
                    'type': 'user_status_changed',
                    'user_id': str(user.id),
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_online': True
                }
            )
            
            # Добавляем пользователя в глобальную группу онлайн
            await self.channel_layer.group_add(
                "online_users",
                self.channel_name
            )
            
        else:
            await self.close()
    
    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None
    
    @database_sync_to_async
    def update_user_status(self, user_id, is_online):
        try:
            status, created = UserOnlineStatus.objects.get_or_create(user_id=user_id)
            status.is_online = is_online
            status.last_activity = timezone.now()
            status.save()
            return status
        except Exception as e:
            print(f"Error updating status: {e}")
            return None
    
    @database_sync_to_async
    def get_online_users_data(self):
        """Возвращает данные онлайн пользователей."""
        return UserOnlineStatus.get_online_users_data()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'user') and self.user:
            # Обновляем статус оффлайн
            await self.update_user_status(self.user.id, False)
            
            # Убираем из групп
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
            await self.channel_layer.group_discard(
                "online_users",
                self.channel_name
            )
            
            # Уведомляем всех об оффлайн пользователе
            await self.channel_layer.group_send(
                "online_users",
                {
                    'type': 'user_status_changed',
                    'user_id': str(self.user.id),
                    'username': self.user.username,
                    'is_online': False
                }
            )
        
        print(f'Disconnected: {close_code}')
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'echo')
            message = data.get('message', '')
            recipient_id = data.get('recipient_id', None)
            
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'ping':
                # Обновляем время последней активности
                await self.update_user_status(self.user.id, True)
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': str(datetime.now())
                }))
            elif message_type == 'get_online_users':
                # Запрос списка онлайн пользователей
                online_users = await self.get_online_users_data()
                await self.send(text_data=json.dumps({
                    'type': 'online_users_list',
                    'online_users': online_users
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'echo',
                    'message': f'Echo: {message}',
                    'user_id': str(self.user.id)  
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
    
    async def handle_chat_message(self, data):
        """Обработка сообщений чата."""
        message = data.get('message', '')
        recipient_id = data.get('recipient_id')
        
        if not recipient_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Recipient ID is required'
            }))
            return
        
        # Получаем данные отправителя для отправки
        sender_data = {
            'id': str(self.user.id),
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
        }
        
        # Получаем аватар отправителя
        avatar_url = await self.get_user_avatar(self.user.id)
        if avatar_url:
            sender_data['avatar_url'] = avatar_url
        
        if self.channel_layer:
            # Отправляем получателю
            await self.channel_layer.group_send(
                f"user_{recipient_id}",
                {
                    'type': 'chat_message',
                    'message_data': {
                        'type': 'chat_message',
                        'message': message,
                        'sender': sender_data,
                        'timestamp': str(datetime.now()),
                        'conversation_id': data.get('conversation_id')
                    }
                }
            )
        
        # Отправляем подтверждение отправителю
        await self.send(text_data=json.dumps({
            'type': 'message_sent',
            'message': message,
            'recipient_id': recipient_id,
            'timestamp': str(datetime.now())
        }))
    
    async def chat_message(self, event):
        """Отправка сообщения клиенту."""
        await self.send(text_data=json.dumps(event['message_data']))
    
    async def user_status_changed(self, event):
        """Обработка изменения статуса пользователя."""
        # Добавляем информацию об аватаре
        avatar_url = None
        if event.get('user_id'):
            avatar_url = await self.get_user_avatar(event['user_id'])
        
        await self.send(text_data=json.dumps({
            'type': 'user_status_changed',
            'user_id': event['user_id'],
            'username': event.get('username', ''),
            'first_name': event.get('first_name', ''),
            'last_name': event.get('last_name', ''),
            'is_online': event['is_online'],
            'avatar_url': avatar_url
        }))
    
    @database_sync_to_async
    def get_user_avatar(self, user_id):
        """Получает URL аватара пользователя."""
        try:
            user = CustomUser.objects.get(id=user_id)
            if user.avatar and user.avatar.image:
                return user.avatar.image.url
            return None
        except CustomUser.DoesNotExist:
            return None
        

  