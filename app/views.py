from django.shortcuts import render
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import subprocess
import os
import json
import uuid

from PIL import Image
from io import BytesIO

import google.generativeai as genai

from .detection_model.detect_chart import detect_chart

import feedparser

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
import logging
from PIL import Image
from io import BytesIO
import base64

from django.contrib.auth.decorators import login_required

@login_required
def indicator(request):
    return render(request, 'indicator.html', {
        'pine_script': YOUR_SCRIPT_STRING  # optional: if you want to render dynamically
    })

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def trading(request):
    return render(request, 'trading.html')

@login_required
def signals(request):
    return render(request, "signals.html")

@login_required
def learn(request):
    return render(request, 'learn.html')

@login_required
def analyze(request):
    return render(request, 'analyze.html')

@login_required
def indicator_view(request):
    return render(request, 'indicator.html')

@login_required
def roadmap_view(request):
    return render(request, 'roadmap.html')

@login_required
def analyze_chart(request):
    if request.method == 'POST' and request.FILES.get('chart_image'):
        chart = request.FILES['chart_image']

        # Save uploaded image
        fs = FileSystemStorage()
        filename = fs.save(f"charts/{chart.name}", chart)
        uploaded_image_path = fs.path(filename)

        # Define YOLO paths
        yolo_path = r"D:\Parmeet\TradeLab\yolov5"  # Updated to new path
        weights_path = os.path.join(yolo_path, 'runs/train/chart-pattern-model2/weights/best.pt')
        output_dir = os.path.join(yolo_path, 'runs/detect/exp_custom')

        # Run detection
        subprocess.run([  
            'python', 'detect.py',
            '--weights', weights_path,
            '--img', '640',
            '--conf', '0.25',
            '--source', uploaded_image_path,
            '--project', os.path.join(yolo_path, 'runs/detect'),
            '--name', 'exp_custom',
            '--exist-ok'
        ], cwd=yolo_path)

        # Prepare result file path
        output_filename = os.path.basename(uploaded_image_path)
        detected_path = os.path.join(output_dir, output_filename)
        final_output = os.path.join(settings.MEDIA_ROOT, f'output_{chart.name}')

        # Move result if exists
        if os.path.exists(detected_path):
            os.replace(detected_path, final_output)
            return render(request, 'analyze.html', {
                'input_image': f'/media/{filename}',
                'output_image': f'/media/output_{chart.name}'
            })
        else:
            return render(request, 'analyze.html', {'error': 'Detection failed. Output file not found.'})

    return render(request, 'analyze.html')


genai.configure(api_key="AIzaSyDbgQ2J6yZzU1UMOAVzx1YQOhhZxqSg-58")

# Text chatbot model (unchanged)
chat_model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Vision model for image analysis
image_model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Add a logger
logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def chatbot_request(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST only"}, status=405)

    # 1. TEXT CHAT HANDLER
    if 'text' in request.POST:
        try:
            user_text = request.POST['text']

            prompt = (
                "You are a helpful trading assistant.\n"
                "Instructions:\n"
                "- Always reply in key points.\n"
                "- Never use bold text.\n"
                "- Keep answers short, clear, and focused.\n"
                f"User: {user_text}"
            )

            resp = chat_model.generate_content(prompt)
            return JsonResponse({"response": resp.text})

        except Exception as e:
            logger.error(f"Text error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    # 2. IMAGE ANALYSIS HANDLER
    if 'image' in request.FILES:
        try:
            logger.info("Image received, starting processing...")

            f = request.FILES['image']
            path = default_storage.save("uploads/tmp.png", ContentFile(f.read()))
            logger.info(f"Image saved to {path}")

            # Convert image to bytes
            img = Image.open(default_storage.path(path)).convert("RGB")
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            image_bytes = buf.getvalue()

            image_input = {
                "mime_type": "image/png",
                "data": image_bytes
            }

            # System instructions for trading chart analysis
            system_prompt = (
                "You are a professional trading analyst. A chart image has been uploaded by the user.\n"
                "Analyze the chart and provide insights as per the instructions below:\n"
                "- Identify key support and resistance levels.\n"
                "- Suggest possible BUY or SELL trade setups.\n"
                "- Include approximate Stop Loss (SL) and Target levels.\n"
                "- Mention any chart patterns visible (e.g., Double Top, Head & Shoulders, Flags, etc).\n"
                "- Respond only in concise key points.\n"
                "- Assume the uploaded image is a trading chart screenshot. Make your response concise, actionable, and focused on helping the trader make a decision\n"
                "- Never write in bold or use long paragraphs.\n"
                "- Keep it relevant to trading decisions only."
            )

            logger.info("Image analysis started...")

            response = image_model.generate_content([system_prompt, image_input])
            logger.info("Image analysis complete.")

            return JsonResponse({"image_analysis": response.text})

        except Exception as e:
            logger.error(f"Image error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "No text or image provided"}, status=400)


@login_required
def roadmap_view(request):
    return render(request, 'roadmap.html')

@login_required
def milestone1(request):
    return render(request, 'roadmap/milestone1.html')

@login_required
def milestone2(request):
    return render(request, 'roadmap/milestone2.html')

@login_required
def milestone3(request):
    return render(request, 'roadmap/milestone3.html')

@login_required
def milestone4(request):
    return render(request, 'roadmap/milestone4.html')

@login_required
def milestone5(request):
    return render(request, 'roadmap/milestone5.html')

@login_required
def milestone6(request):
    return render(request, 'roadmap/milestone6.html')

@login_required
def milestone7(request):
    return render(request, 'roadmap/milestone7.html')

@login_required
def milestone8(request):
    return render(request, 'roadmap/milestone8.html')


@login_required
def market_news(request):
    categories = {
        'forex': 'https://www.investing.com/rss/news_301.rss',  
    }

    all_news = []
    categorized_news = {}

    for name, url in categories.items():
        feed = feedparser.parse(url)
        print(f"Fetched {name} feed:", feed.entries)  # Debugging line
        items = feed.entries[:10]  # Get top 8 per category
        categorized_news[name] = items
        all_news.extend(items)

    all_news.sort(key=lambda x: x.published_parsed, reverse=True)

    return render(request, 'news.html', {
        'categorized_news': categorized_news,
        'all_news': all_news
    })


@login_required
def market_timings(request):
    return render(request, 'markets.html')


@login_required
def crypto_market(request):
    return render(request, 'markets/crypto.html')

@login_required
def forex_market(request):
    return render(request, 'markets/forex.html')

@login_required
def indian_market(request):
    return render(request, 'markets/indian.html')

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Username validation
        if username and len(username) < 5:
            self.add_error('username', "Username must be at least 5 characters.")
        elif User.objects.filter(username=username).exists():
            self.add_error('username', "Username already taken.")

        # Password validation
        if password1 and len(password1) < 6:
            self.add_error('password1', "Password must be at least 6 characters.")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('login')  # Redirect to login page after success
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def signup_success(request):
    return render(request, 'signup_success.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            

            error_message = "Invalid username or password"
    return render(request, 'login.html', {'error_message': error_message})