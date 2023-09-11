from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

import os
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone

openai_api_key = "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"  # Replace YOUR_API_KEY with your openai apikey
openai.api_key = openai_api_key
conversation_so_far = []

WORK_DIR = "/Users/qianhuisun/Desktop/Chatbot/django-chatgpt-chatbot/chatbot"
CONTENT_FILE_NAME = "system_message2.txt"


def get_system_message_content():
    try:
        content_path = os.path.join(WORK_DIR, CONTENT_FILE_NAME)
        with open(content_path, "r") as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"Error: {e}")


SYSTEM_PROMT = get_system_message_content()


def clear_chat(request):
    if request.user.is_authenticated:
        Chat.objects.filter(user=request.user).delete()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "User not authenticated"})


def ask_openai(user_message, assistant_message, message):
    system_message_content = SYSTEM_PROMT
    messages = [
        {
            "role": "system",
            "content": system_message_content,  # system message
        },
    ]

    # Append the conversation_so_far to messages
    for i in range(len(user_message)):
        messages.append({"role": "user", "content": user_message[i]})
        messages.append({"role": "assistant", "content": assistant_message[i]})
    messages.append({"role": "user", "content": message})

    print("!!!!--API messages", messages)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    try:
        answer = response.choices[0].message["content"].strip()
        print(answer)
        return answer
    except openai.error.OpenAIError as e:
        return str(e)


user_message = []
assistant_message = []


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        # message is user input
        message = request.POST.get("message")
        # response is one line
        response = ask_openai(user_message, assistant_message, message)
        user_message.append(message)
        assistant_message.append(response)
        print("!!!!!!!CONVERSATION!!!!!!", conversation_so_far)
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
