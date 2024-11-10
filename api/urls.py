from django.urls import path
from .views import OpenAIAPConversationIView, OpenAIAPEmotionIView

urlpatterns = [
    path('openai-conversation/', OpenAIAPConversationIView.as_view(), name='openai-api-conversation'),
    path('openai-emotion/', OpenAIAPEmotionIView.as_view(), name='openai-api-emotion'),
]
