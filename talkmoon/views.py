from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import pytesseract
import requests
import io
from gtts import gTTS
import base64

def text_to_base64_audio(text):
    tts = gTTS(text=text, lang='pt')
    with io.BytesIO() as buffer:
        tts.write_to_fp(buffer)  # Use write_to_fp para escrever no buffer
        buffer.seek(0)  # Volta para o início do buffer
        audio_data = buffer.read()
        audio_str = base64.b64encode(audio_data).decode('utf-8')
    return audio_str


def convert_image(request):
    if request.method == 'POST':
        image_url = request.POST.get('image_url')
        
        response = requests.get(image_url)

        # Verifica se o download foi bem-sucedido e se o conteúdo é uma imagem
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            try:
                # Tenta abrir a imagem
                image = Image.open(io.BytesIO(response.content))
                
                # Realiza o OCR para extrair texto
                text = pytesseract.image_to_string(image, lang='por')

                audio_base64 = text_to_base64_audio(text)

                # Passa o texto extraído e o áudio para o template
                return render(request, 'talkmoon/index.html', {'result': text, 'audio_base64': audio_base64})
                
            except Image.UnidentifiedImageError:
                return HttpResponse("Erro: Não foi possível identificar o arquivo de imagem.")
        else:
            return HttpResponse("Erro: O download falhou ou o conteúdo não é uma imagem.")
    else:
        return render(request, 'talkmoon/index.html')
