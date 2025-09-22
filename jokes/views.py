from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import qrcode
from io import BytesIO
import base64
from ciphers.utils import CipherUtils
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from .serializers import JokeRequestSerializer, JokeResponseSerializer


@login_required
def jokes_dashboard_view(request):
    """Jokes dashboard with QR code generation"""
    return render(request, 'jokes/jokes_dashboard.html')


@swagger_auto_schema(
    method='get',
    operation_description="Fetch a random joke from JokeAPI with QR code generation",
    responses={
        200: JokeResponseSerializer,
        400: "Bad Request",
        500: "Internal Server Error"
    },
    tags=['jokes']
)
@api_view(['GET'])
@login_required
def fetch_joke(request):
    """Fetch a random joke from JokeAPI"""
    try:
        # Fetch joke from JokeAPI
        response = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
        joke_data = response.json()
        
        # Format joke text
        if joke_data.get('type') == 'single':
            joke_text = joke_data.get('joke', '')
        else:
            setup = joke_data.get('setup', '')
            delivery = joke_data.get('delivery', '')
            joke_text = f"{setup}\n\n{delivery}"
        
        # Generate QR codes for original and encrypted versions
        qr_codes = {}
        
        # Original joke QR code
        qr_codes['original'] = generate_qr_code(joke_text)
        
        # Atbash encrypted
        atbash_text = CipherUtils.atbash_cipher(joke_text)
        qr_codes['atbash'] = generate_qr_code(atbash_text)
        
        # Caesar encrypted (shift=3)
        caesar_text = CipherUtils.caesar_cipher(joke_text, shift=3)
        qr_codes['caesar'] = generate_qr_code(caesar_text)
        
        # Vigenere encrypted (key="JOKE")
        vigenere_text = CipherUtils.vigenere_cipher(joke_text, key="JOKE")
        qr_codes['vigenere'] = generate_qr_code(vigenere_text)
        
        return JsonResponse({
            'success': True,
            'joke': joke_text,
            'category': joke_data.get('category', 'Unknown'),
            'encrypted': {
                'atbash': atbash_text,
                'caesar': caesar_text,
                'vigenere': vigenere_text
            },
            'qr_codes': qr_codes
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def generate_qr_code(text):
    """Generate QR code from text and return base64 encoded image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"
