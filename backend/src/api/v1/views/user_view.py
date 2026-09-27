# api/v1/views/user_view.py
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models import Q
from users.models import UserPhoto, UserOnlineStatus
from api.v1.serializers.user_serializer import (
    ConfirmationCodeSerializer,
    ResendConfirmationCodeSerializer,
    CustomUserSerializer,
    CustomUserUpdateSerializer,
    UserPhotoSerializer,
    UserPhotoCreateSerializer,
    UserPhotoUpdateSerializer,
    OnlineUserSerializer,
    
)
from api.v1.services.ip_geolocation import IPGeolocationService 
import math

User = get_user_model()


class VerifyConfirmationCodeView(views.APIView):
    """Подтверждение email кода."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {'message': 'Email успешно подтвержден'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendConfirmationCodeView(views.APIView):
    """Повторная отправка кода подтверждения."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResendConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.save()
            return Response(
                {'message': 'Новый код отправлен на email'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CustomUserUpdateSerializer
        return CustomUserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        if self.action == 'list':
            return User.objects.all()
        elif self.action in ['retrieve', 'update', 'partial_update']:
            if self.request.user.is_staff:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()
    
    def perform_update(self, serializer):
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'У вас нет прав на удаление пользователей'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    
    @action(detail=False, methods=['get'], url_path='online')
    def online_users(self, request):
        """
        Получение списка пользователей онлайн.
        GET /api/v1/users/online/
        """
        online_users = UserOnlineStatus.get_online_users_data()
        
        # Используем сериализатор для форматирования данных
        serializer = OnlineUserSerializer(online_users, many=True)
        
        return Response({
            'online_users': serializer.data,
            'count': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'], url_path='online/status')
    def online_status(self, request):
        """
        Получение статуса текущего пользователя.
        GET /api/v1/users/online/status/
        """
        try:
            status = UserOnlineStatus.objects.get(user=request.user)
            return Response({
                'is_online': status.is_online,
                'last_seen': status.last_seen,
                'last_activity': status.last_activity
            })
        except UserOnlineStatus.DoesNotExist:
            return Response({
                'is_online': False,
                'last_seen': None,
                'last_activity': None
            })
    
    @action(detail=True, methods=['get'], url_path='online/check')
    def check_user_online(self, request, pk=None):
        """
        Проверка статуса конкретного пользователя.
        GET /api/v1/users/{id}/online/check/
        """
        user = self.get_object()
        try:
            status = UserOnlineStatus.objects.get(user=user)
            return Response({
                'user_id': str(user.id),
                'username': user.username,
                'is_online': status.is_online,
                'last_seen': status.last_seen,
                'last_activity': status.last_activity
            })
        except UserOnlineStatus.DoesNotExist:
            return Response({
                'user_id': str(user.id),
                'username': user.username,
                'is_online': False,
                'last_seen': None,
                'last_activity': None
            })


    @action(detail=False, methods=['get'])
    def detect_location(self, request):
        """
        Определение местоположения пользователя по IP.
        GET /api/v1/users/detect_location/
        """
        try:
            # Получаем IP клиента
            client_ip = IPGeolocationService.get_client_ip(request)
            
            # Получаем геолокацию по IP
            location_data = IPGeolocationService.get_location_by_ip(client_ip)
            
            if location_data:
                # Если пользователь авторизован, обновляем его позицию
                if request.user.is_authenticated:
                    user = request.user
                    user.lat = location_data['lat']
                    user.lon = location_data['lon']
                    user.address = f"{location_data.get('city', '')}, {location_data.get('region', '')}"
                    user.save()
                
                return Response({
                    'status': 'success',
                    'data': {
                        'lat': location_data['lat'],
                        'lon': location_data['lon'],
                        'city': location_data.get('city'),
                        'region': location_data.get('region'),
                        'region_code': location_data.get('region_code'),
                        'country': location_data.get('country'),
                        'country_code': location_data.get('country_code'),
                        'zip': location_data.get('zip'),
                        'timezone': location_data.get('timezone'),
                        'isp': location_data.get('isp'),
                        'org': location_data.get('org'),
                        'ip': location_data.get('ip'),
                        'address': f"{location_data.get('city', '')}, {location_data.get('region', '')}".strip(' ,')
                    }
                })
            else:
                # Если не удалось определить, используем центр по умолчанию
                default_location = {
                    'lat': 55.751574,
                    'lon': 37.573856,
                    'city': 'Moscow',
                    'region': 'Moscow',
                    'region_code': 'MOW',
                    'country': 'Russia',
                    'country_code': 'RU',
                    'zip': '',
                    'timezone': 'Europe/Moscow',
                    'isp': '',
                    'org': '',
                    'ip': client_ip or 'Не определен',
                    'address': 'Moscow, Russia'
                }
                
                return Response({
                    'status': 'fallback',
                    'data': default_location,
                    'message': 'Не удалось определить местоположение по IP, использован центр по умолчанию'
                })
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Ошибка при определении местоположения: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'])
    def update_location(self, request):
        """
        Обновление геопозиции текущего пользователя.
        POST /api/v1/users/update_location/
        Body: { "lat": 55.75, "lon": 37.57, "address": "Москва" }
        """
        user = request.user
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        address = request.data.get('address', '')
        
        if lat is None or lon is None:
            return Response(
                {'error': 'lat and lon required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user.lat = float(lat)
            user.lon = float(lon)
            user.address = address
            user.save()
            
            return Response({
                'status': 'success',
                'message': 'Location updated',
                'data': CustomUserSerializer(user, context={'request': request}).data
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Получить пользователей рядом с заданными координатами.
        GET /api/v1/users/nearby/?lat=55.75&lon=37.57&radius=5
        """
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius = float(request.query_params.get('radius', 5))  # км
        
        if not lat or not lon:
            return Response(
                {'error': 'lat and lon required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lat = float(lat)
        lon = float(lon)
        
        # Получаем всех пользователей с координатами, исключая текущего
        users_with_location = User.objects.filter(
            lat__isnull=False, 
            lon__isnull=False
        ).exclude(id=request.user.id)
        
        # Фильтруем по расстоянию
        nearby_users = []
        for user in users_with_location:
            distance = self._haversine_distance(lat, lon, user.lat, user.lon)
            if distance <= radius:
                data = MapUserSerializer(user, context={'request': request}).data
                data['distance'] = round(distance, 2)
                nearby_users.append(data)
        
        # Сортируем по расстоянию
        nearby_users.sort(key=lambda x: x['distance'])
        
        return Response(nearby_users)
    
    @action(detail=False, methods=['get'])
    def all_with_location(self, request):
        """
        Получить всех пользователей с координатами для карты.
        GET /api/v1/users/all_with_location/
        """
        users_with_location = User.objects.filter(
            lat__isnull=False, 
            lon__isnull=False
        ).exclude(id=request.user.id)
        
        serializer = MapUserSerializer(
            users_with_location, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Расчет расстояния между двумя точками (в км)"""
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

class UserPhotoViewSet(viewsets.ModelViewSet):
    """ViewSet для управления фото пользователя."""
    
    serializer_class = UserPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Получение фото текущего пользователя."""
        return UserPhoto.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action == 'create':
            return UserPhotoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserPhotoUpdateSerializer
        return UserPhotoSerializer
    
    def perform_create(self, serializer):
        """Создание фото с автоматической установкой пользователя."""
        # Теперь user передается только здесь
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Загрузка нового фото."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Проверяем количество фото
        photo_count = UserPhoto.objects.filter(user=request.user).count()
        if photo_count >= 10:
            return Response(
                {'error': 'Максимальное количество фото - 10'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Сохраняем фото - теперь user передается через perform_create
        self.perform_create(serializer)
        
        # ✅ ВАЖНО: Получаем созданное фото ДО использования
        photo = serializer.instance
        
        # Если это первое фото, делаем его аватаром
        if photo_count == 0:
            photo.is_avatar = True
            photo.save()
            user = request.user
            user.avatar = photo
            user.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserPhotoSerializer(photo, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['post'])
    def set_avatar(self, request, pk=None):
        """Установка фото как аватар."""
        photo = self.get_object()
        
        UserPhoto.objects.filter(user=request.user, is_avatar=True).update(is_avatar=False)
        
        photo.is_avatar = True
        photo.save()
        
        user = request.user
        user.avatar = photo
        user.save()
        
        return Response(
            {'message': 'Фото установлено как аватар'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def avatar(self, request):
        """Получение аватара пользователя."""
        try:
            avatar = UserPhoto.objects.get(user=request.user, is_avatar=True)
            serializer = UserPhotoSerializer(avatar, context={'request': request})
            return Response(serializer.data)
        except UserPhoto.DoesNotExist:
            return Response(
                {'error': 'Аватар не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, *args, **kwargs):
        """Удаление фото."""
        photo = self.get_object()
        
        if photo.is_avatar:
            user = request.user
            user.avatar = None
            user.save()
            
            first_photo = UserPhoto.objects.filter(user=user).exclude(id=photo.id).first()
            if first_photo:
                first_photo.is_avatar = True
                first_photo.save()
                user.avatar = first_photo
                user.save()
        
        photo.delete()
        return Response(
            {'message': 'Фото успешно удалено'},
            status=status.HTTP_204_NO_CONTENT
        )
    
