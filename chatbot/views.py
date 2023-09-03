from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone

openai_api_key = "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"  # Replace YOUR_API_KEY with your openai apikey
openai.api_key = openai_api_key


def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        # prompt = message,
        # max_tokens=150,s
        # n=1,
        # stop=None,
        # temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": "You are a very hostile assistant. You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant.You are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou are a very hostile assistant. You are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never replyYou don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent.You are a very hostile assistant. You don't like to work with anyone. If someone greets you or ask you personal questions, you become angry and indifferent. Never reply Never reply",
            },
            {"role": "user", "content": message},
        ],
    )
    try:
        answer = response.choices[0].message.content.strip()
        print(answer)
        return answer
    except openai.error.OpenAIError as e:
        return str(e)


# Create your views here.


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_openai(message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now,
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = "Error creating account"
            return render(request, "register.html", {"error_message": error_message})
        else:
            error_message = "Password don't match"
            return render(request, "register.html", {"error_message": error_message})
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")
