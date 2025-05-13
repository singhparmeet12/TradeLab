from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import login_view

# from . import upload_view 


urlpatterns = [
    path('', views.home, name='home'),
    path('trading/', views.trading, name='trading'),
    path('signals/', views.signals, name='signals'),
    path('learn/', views.learn, name='learn'),
    path('analyze/', views.analyze_chart, name='analyze_chart'),
    path('indicator/', views.indicator_view, name='indicator'),
    path('api/chatbot/', views.chatbot_request, name='chatbot_request'),
    path('learn/roadmap/', views.roadmap_view, name='trading_roadmap'),
     path('learn/roadmap/', views.roadmap_view, name='roadmap'),
    path('milestone1/', views.milestone1, name='milestone1'),
    path('milestone2/', views.milestone2, name='milestone2'),
    path('milestone3/', views.milestone3, name='milestone3'),
    path('milestone4/', views.milestone4, name='milestone4'),
    path('milestone5/', views.milestone5, name='milestone5'),
    path('milestone6/', views.milestone6, name='milestone6'),
    path('milestone7/', views.milestone7, name='milestone7'),
    path('milestone8/', views.milestone8, name='milestone8'),
    path('news/', views.market_news, name='market_news'),
    path('markets/', views.market_timings, name='markets'),
    path('crypto/', views.crypto_market, name='crypto_market'),
    path('forex/', views.forex_market, name='forex_market'),
    path('indian/', views.indian_market, name='indian_market'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', login_view, name='login'),
  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('signup-success/', views.signup_success, name='signup_success'),
    

 ]
