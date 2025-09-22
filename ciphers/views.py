from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import CipherUtils
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from .serializers import CipherRequestSerializer, CipherResponseSerializer


@login_required
def cipher_tools_view(request):
    """Main cipher tools page"""
    return render(request, 'ciphers/cipher_tools.html')


@swagger_auto_schema(
    method='post',
    request_body=CipherRequestSerializer,
    operation_description="Process text with specified cipher algorithm",
    responses={
        200: CipherResponseSerializer,
        400: "Bad Request",
        500: "Internal Server Error"
    },
    tags=['ciphers']
)
@api_view(['POST'])
@login_required
@csrf_exempt
def process_cipher(request):
    """API endpoint to process cipher encryption/decryption"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            cipher_type = data.get('cipher_type', 'caesar')
            mode = data.get('mode', 'encrypt')
            
            # Additional parameters
            shift = data.get('shift', 3)
            key = data.get('key', 'KEY')
            
            # Process the text
            result = CipherUtils.process_text(
                text=text,
                cipher_type=cipher_type,
                mode=mode,
                shift=shift,
                key=key
            )
            
            return JsonResponse({
                'success': True,
                'result': result,
                'original': text,
                'cipher_type': cipher_type,
                'mode': mode
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
