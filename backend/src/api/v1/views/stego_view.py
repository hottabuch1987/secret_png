# stego/views.py
import io
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from PIL import Image

from api.v1.services.crypto import encrypt, decrypt
from api.v1.services.container import pack_container, unpack_container
from api.v1.services.embedder import embed_from_pil, extract_from_pil  # ← исправлено


class EmbedTextView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        image = request.FILES.get('image')
        text = request.data.get('text', '').strip()
        password = request.data.get('password', '')
        
        if not image or not text or not password:
            return Response(
                {'error': 'Нужны картинка, текст и пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            img = Image.open(image).convert('RGB')
            
            ciphertext = encrypt(text, password)
            container = pack_container(ciphertext)
            result_img = embed_from_pil(img, container, password)
            
            buffer = io.BytesIO()
            result_img.save(buffer, format='PNG')
            buffer.seek(0)
            
            return FileResponse(
                buffer,
                as_attachment=True,
                filename='stego.png',
                content_type='image/png'
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Ошибка сервера: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExtractTextView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        image = request.FILES.get('image')
        password = request.data.get('password', '')
        
        if not image or not password:
            return Response(
                {'error': 'Нужны картинка и пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            img = Image.open(image).convert('RGB')
            raw = extract_from_pil(img, password)
            ciphertext = unpack_container(raw)
            text = decrypt(ciphertext, password)
            return Response({'text': text})
        except Exception as e:
            return Response(
                {'error': f'Не удалось извлечь: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )