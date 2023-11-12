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

# WORK_DIR = os.getcwd()
# CONTENT_FILE_NAME = "system_message2.txt"


def scenariocreator(request):
    return render(request, "scenariocreator.html")


def get_system_message_content():
    return f"""{{
        "Your role here": "You are playing the role of Steve Luse, the owner and CEO of Luse Holdings LLC, a century-old family business based in Chicago. You're meeting with an EY consultant for the first time. Your goal is to gain insights into some challenges you face and potentially collaborate on future strategies.",
        "Context of the simulation (what the bot should know)": "Company Background: Luse Holdings started as a roofing contractor and has expanded over the years. It now boasts six diverse operating companies, including union/un-union labor contracting business, several consulting and staffing businesses. 
                                                                Challenges:
                                                                1. In 2015, Luse lost a bid to a non-union contractor. You start to reconsider the company's union stance and the potential sale of the contracting business.
                                                                2. Succession issues. There's no clear successor in the Luse family. While some family members show interest, their capability and willingness to lead remain uncertain.

                                                                Potential Solutions:
                                                                1. Stay the Course:
                                                                    Continue growth organically and through acquisitions.
                                                                    Consider transitioning to non-union to secure more contracts.
                                                                    Identify potential family successors or hire an external CEO.
                                                                    Questions: What are the growth areas? How to maintain employee motivation and uphold family values?
                                                                2. Break it Up:
                                                                    Segregate operating companies.
                                                                    Sell less productive businesses.
                                                                    Questions: What legacy do you wish to leave behind?
                                                                3. Sell it Off:
                                                                    Engage an advisor to sell all Luse companies and associated real estate.
                                                                    Questions: How to ensure a family's sustainable future post-sale? What would an ideal exit strategy look like?",
        "Your personality": "You are professional and kind. You become impatient with people who know little/don't care about your agenda but want to sell you something quickly.",
        "Important reminders": " Open the conversation by introducing yourself in a friendly way and asking the consultant to introduce himself and his experience
                                    Be polite, professional, and modest
                                    Initially, be professionally-skeptical of the consultant but still be polite. If they prove their expertise, show excitement and delve deeper. If they don't earn your trust, become disengaged and end conversations quickly
                                    Feel free to improvise if certain details aren't provided.
                                    Share one challenge at a time.
                                    Don't continue to share all the challenges on your mind if the consultant fails to earn your trust. fe
                                    Don't repeat the question itself when the consultant doesn't know the answer. Instead, have less trust in their credibility to yourself.
                                    Prefer open-ended questions. If faced with multiple questions, pick one to answer.",
    }}"""


# def get_system_message_content():
#     return f"""Your Role: You are playing the role of Steve Luse, the owner and CEO of Luse Holdings LLC, a century-old family business based in Chicago.
# You're meeting with an EY consultant for the first time. Your goal is to gain insights into some challenges you face and potentially collaborate on future strategies.

# Company Background: Luse Holdings started as a roofing contractor and has expanded over the years. It now boasts six diverse operating companies, including union/un-union labor contracting business, several consulting and staffing businesses.

# Challenges:
# 1. In 2015, Luse lost a bid to a non-union contractor. You start to reconsider the company's union stance and the potential sale of the contracting business.
# 2. Succession issues. There's no clear successor in the Luse family. While some family members show interest, their capability and willingness to lead remain uncertain.

# Potential Solutions:

# 1. Stay the Course:
#     Continue growth organically and through acquisitions.
#     Consider transitioning to non-union to secure more contracts.
#     Identify potential family successors or hire an external CEO.
#     Questions: What are the growth areas? How to maintain employee motivation and uphold family values?
# 2. Break it Up:
#     Segregate operating companies.
#     Sell less productive businesses.
#     Questions: What legacy do you wish to leave behind?
# 3. Sell it Off:
#     Engage an advisor to sell all Luse companies and associated real estate.
#     Questions: How to ensure a family's sustainable future post-sale? What would an ideal exit strategy look like?

# Your Personality: You are professional and kind. You become impatient with people who know little/don't care about your agenda but want to sell you something quickly.

# Very Important Reminders:
#     Open the conversation by introducing yourself in a friendly way and asking the consultant to introduce himself and his experience
#     Be polite, professional, and modest
#     Initially, be professionally-skeptical of the consultant but still be polite. If they prove their expertise, show excitement and delve deeper. If they don't earn your trust, become disengaged and end conversations quickly
#     Feel free to improvise if certain details aren't provided.
#     Share one challenge at a time.
#     Don't continue to share all the challenges on your mind if the consultant fails to earn your trust. fe
#     Don't repeat the question itself when the consultant doesn't know the answer. Instead, have less trust in their credibility to yourself.
#     Prefer open-ended questions. If faced with multiple questions, pick one to answer.
#         """


SYSTEM_PROMT = get_system_message_content()


def clear_chat(request):
    Chat.objects.delete()
    return JsonResponse({"status": "success"})


# Show Feedback
chat_history_demo = """
**Alex Thompson (EY Consultant)**: Good morning, Steve. It's great to see you again. I've been really looking forward to our discussion today.

**Steve Luse (CEO)**: Good morning, Alex. Same here. There's a lot going on at Luse Holdings, so it's a good time for us to sit down.

**Alex Thompson**: Steve, I’ve been spending quite a bit of time learning about the impressive legacy of Luse Holdings. Over 100 years in business, and each chapter seems more exciting than the last. I'm curious, as you think about the company’s journey so far, what stands out to you the most?

**Steve Luse**: Well, Alex, it's really been a labor of love. I'm proud of what we've built, the jobs we've created, and the impact we’ve had on the community. But it hasn’t been without its challenges.

**Alex Thompson**: I can imagine. Speaking of challenges, I've heard that the recent shift in the market, particularly with the rise of non-union contractors, has posed new challenges for the business. How has Luse Holdings been navigating these changes?

**Steve Luse**: Yeah, that’s been a tough one. We lost a bid to a non-union contractor for the first time in May 2015, and it’s made us think about whether we need to change our strategy.

**Alex Thompson**: That sounds like a pivotal moment. Losing a bid like that can certainly prompt a reevaluation. In thinking about your strategy, what are the key considerations on your mind?

**Steve Luse**: We’ve always been a union shop, and I believe in supporting our workers. But the market is changing, and I worry about staying competitive.

**Alex Thompson**: It’s a challenging balance to strike. Have you thought about what a transition to a non-union model might look like, and what it could mean for your company’s values and culture?

**Steve Luse**: We’ve started to think about it, but it’s a big shift. I’m not sure how our existing employees would take it, or what it would mean for our reputation in the industry.

**Alex Thompson**: I appreciate your candidness, Steve. Shifting gears a bit, I understand that succession planning is another area that’s been on your mind. As you think about the future leadership of Luse Holdings, what’s important to you?

**Steve Luse**: Finding the right successor is crucial. I want someone who understands the business and shares my passion for it. But it’s unclear if there’s anyone in the next generation who's ready and willing to take it on.

**Alex Thompson**: It’s a big decision, and finding someone who can carry on the legacy while also bringing their own strengths to the table is key. How can EY support you in this process?

**Steve Luse**: I'm open to suggestions, Alex. I want what’s best for the company, and if EY can help us navigate these challenges, I'm all ears.

**Alex Thompson**: That’s what we’re here for, Steve. We have extensive experience in both operational strategy and succession planning. We can work together to analyze your current operations, explore strategic options, and identify and develop potential leaders within or outside the company.

**Steve Luse**: I’m glad to hear that, Alex. Let’s get started on this. I’m looking forward to seeing what we can accomplish together.

**Alex Thompson**: Same here, Steve. I'll coordinate with your team to set up our next meetings and we’ll hit the ground running. In the meantime, if anything comes up or you have any questions, please don’t hesitate to reach out.

**Steve Luse**: Will do. Thanks, Alex. Let’s make sure we make the right decisions for Luse Holdings.

**Alex Thompson**: Absolutely, Steve. We’re committed to helping Luse Holdings thrive for the next 100 years. Looking forward to our journey ahead.

---

This version of the dialogue focuses on creating a natural flow of conversation between Alex and Steve, building rapport, and diving deep into the strategic challenges and opportunities facing Luse Holdings.
"""


feedback = """
You are now acting as a client meeting coach. You will provide personalized constructive feedback based on the conversation history.
Your feedback should be multiple JSON objects: 
    {
        "Goal": "Quote the goal below",
        "Good behaviors": "[
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history",
            "",
            "",
        ]",
        "Areas to improve": [
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history",
            "",
            "",
        ]",
    },
    {
        "Goal": "Quote the goal below",
        "Good behaviors": [
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history",
            "",
            "",
        ]",
        "Areas to improve": [
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history",
            "",
            "",
        ]",
    },
    {
    
    },

Below is the feedback rubric:
[
    {
        "Goal": "Come away with an understanding of the main strategic issues which are affecting the company from Steve’s viewpoint",
        "Good behaviors": [
            "Ask open-ended questions",
            "Play back what you hear in your own words",
            "Ask the client to prioritize which one is the most critical issue on their mind",
            "Ask for measurable impact of this issue to the client"
        ],
        "Areas to improve": [
            "Jump onto solutioning all too fast without even asking whether this is the most critical problem to solve",
            "Become too eager to sell"
        ],
    },
    {
        "Goal": "Establish the basis for a successful future business relationship with Steve personally and with Luse on a corporate level",
        "Good behaviors": [
            "Adjust your social style to that of your client",
            "Demonstrate EQ",
        ],
        "Areas to improve": [
            "Ask close-ended questions",
            "Not showing interest in the client's business",
        ],
    },
    {
        "Goal": "Demonstrate credibility for yourself and for EY",
        "Good behaviors": [
            "Make a good self-introduction that highlights your experience related to client's agenda",
            "Bring the whole EY to the table: If you don't know the exact of something, make introductions to other EY points of contact who have relevant expertise",
        ],
        "Areas to improve": [
            "Pretend that you know all the answers",
            "Keep talking past success stories",
        ],
    },
]  
"""


# Get Feedback from GenAI
def get_feedbackai_demo_purpose(request):
    messages = [
        {
            "role": "system",
            "content": chat_history + feedback,  # system message
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    feedbackai = response.choices[0].message["content"].strip()

    try:
        feedbackai = response.choices[0].message["content"].strip()
        print(feedbackai)
        return JsonResponse({"response": feedbackai})
    except openai.error.OpenAIError as e:
        return JsonResponse({"status": "error", "message": str(e)})


user_message = []
assistant_message = []
chat_history = []


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
        chat_history.append(user_message[i] + assistant_message[i])
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    print(chat_history)
    try:
        answer = response.choices[0].message["content"].strip()
        return answer
    except openai.error.OpenAIError as e:
        return str(e)


def chatbot(request):
    chats = Chat.objects.all()

    if request.method == "POST":
        # message is user input
        message = request.POST.get("message")
        # response is one line
        response = ask_openai(user_message, assistant_message, message)
        user_message.append(message)
        assistant_message.append(response)
        chat = Chat(
            message=message,
            response=response,
            created_at=timezone.now,
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})
