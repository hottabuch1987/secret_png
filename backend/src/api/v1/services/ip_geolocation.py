# api/v1/services/ip_geolocation.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class IPGeolocationService:
    """Сервис для определения геолокации по IP через ip-api.com"""
    
    BASE_URL = "http://ip-api.com/json/"
    
    @classmethod
    def get_location_by_ip(cls, ip=None):
        """
        Получение геолокации по IP адресу.
        """
        try:
            # Формируем URL с параметрами
            url = f"{cls.BASE_URL}{ip if ip else ''}?fields=61439"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'city': data.get('city'),
                    'region': data.get('regionName'),  # Используем regionName для полного названия
                    'region_code': data.get('region'),  # Код региона
                    'country': data.get('country'),
                    'country_code': data.get('countryCode'),
                    'zip': data.get('zip'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'as': data.get('as'),
                    'ip': data.get('query')
                }
            else:
                logger.warning(f"IP API error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error getting location by IP: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in IP geolocation: {e}")
            return None
    
    @classmethod
    def get_client_ip(cls, request):
        """Получение реального IP клиента из request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Если IP локальный (для разработки), используем тестовый
        if ip in ['127.0.0.1', 'localhost', '::1']:
            # Можно вернуть None, чтобы ip-api.com использовал IP сервера
            # или использовать какой-то тестовый IP
            return None
        
        return ip