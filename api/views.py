import openai
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OpenAIRequestSerializer

openai.api_key = settings.OPENAI_API_KEY
emotionPrompt = settings.EMOTION_PROMPT
conversationPrompt = settings.CONVERSATION_PROMPT

def get_openai_response(prompt, text):
    """
    OpenAI APIにリクエストを送信し、レスポンスを取得します

    Args:
        prompt (str): システムメッセージとして使用するプロンプト
        text (str): ユーザーからの入力テキスト。

    Returns:
        str: OpenAIからの応答メッセージ
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def emotion_scoring(text):
    """
    テキストから感情スコアを抽出します

    Args:
        text (str): 感情スコアを含むテキスト

    Returns:
        dict: 各感情のスコアを含む辞書
    """
    parts = text.split(" ")
    happy = anger = sadness = joy = 0

    for i in range(0, len(parts), 2):
        keyword = parts[i]
        value = float(parts[i + 1])

        if keyword == "喜":
            happy = value
        elif keyword == "怒":
            anger = value
        elif keyword == "哀":
            sadness = value
        elif keyword == "楽":
            joy = value

    score = {
        "happy": happy,
        "anger": anger,
        "sadness": sadness,
        "joy": joy
    }

    return score

class OpenAIAPConversationIView(APIView):
    """
    ユーザーの入力に基づいたOpenAIの返答を返すAPI
    """
    def post(self, request):
        serializer = OpenAIRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            message_content = get_openai_response(conversationPrompt, text)
            return Response({'message': message_content}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OpenAIAPEmotionIView(APIView):
    """
    ユーザーの入力に基づいて感情スコアを計算するAPI
    """
    def post(self, request):
        serializer = OpenAIRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            message_content = get_openai_response(emotionPrompt, text)

            score = emotion_scoring(message_content)

            return Response({'score': score}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
