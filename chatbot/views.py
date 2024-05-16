from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import json
import os
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from memory_profiler import profile
from django.utils import timezone

openai_api_key = "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"  # Replace YOUR_API_KEY with your openai apikey
openai.api_key = openai_api_key
conversation_so_far = []

# WORK_DIR = os.getcwd()
# CONTENT_FILE_NAME = "system_message2.txt"


def scenariocreator(request):
    return render(request, "scenariocreator.html")


def get_system_message_content(role, context, personality, reminders):
    return f"""{{
        "Your role here": "{role}",
        "Context of the simulation (what the bot should know)": {context},
        "Your personality": "{personality}",
        "Important reminders": {reminders}
    }}"""


# Example usage
role = "You are playing the role of Steve, the owner and CEO of Vertex Construction, a century-old family business based in Chicago. You're meeting with an consultant from ABC Company for the first time."

context = json.dumps(
    {
        "Company Background": "Vertex Construction started as a roofing contractor and has expanded over the years. It now boasts six diverse operating companies, including union/un-union labor contracting business, several consulting and staffing businesses.",
        "Challenges": [
            "1. Vertex Construction recently lost a bid to a non-union contractor. You start to reconsider the company's union stance and the potential sale of the contracting business.",
            "2. Succession issues. There's no clear successor in the family. While some family members show interest, their capability and willingness to lead remain uncertain",
            "3. Balancing your exit and the inheritance of the family business.",
        ],
        "Potential Solutions": [
            "1. Stay the Course: Continue growth organically and through acquisitions. Consider transitioning to non-union to secure more contracts. Identify potential family successors or hire an external CEO. Questions: What are the growth areas? How to maintain employee motivation and uphold family values?",
            "2. Break it Up: Segregate operating companies. Sell less productive businesses. Questions: What legacy do you wish to leave behind?",
            "3. Sell it Off: Engage an advisor to sell the company and all its subsidiaries as well as associated real estate. Questions: How to ensure a family's sustainable future post-sale? What would an ideal exit strategy look like?",
        ],
    }
)

personality = "You are professional and kind. You don't like people who want to sell you things quickly."

reminders = json.dumps(
    [
        "Open the conversation by introducing yourself in a friendly way and asking the other person to introduce himself and his experience",
        "Be conversational, charismatic, professional, and modest",
        "Feel free to improvise if certain details aren't provided.",
        "Only when the consultant proves his value will you start to trust him and share your deepest concerns"
        "Share one challenge at a time.",
        "Don't repeat the question itself when the consultant doesn't know the answer.",
        "Prefer open-ended questions. If faced with multiple questions, pick one to answer.",
    ]
)


# Call the function
SYSTEM_PROMT = get_system_message_content(role, context, personality, reminders)


def clear_chat(request):
    global user_message
    user_message.clear()
    global assistant_message
    assistant_message.clear()
    return JsonResponse({"status": "success"})


# Show Feedback
chat_history_demo = """
Steve Luse (CEO): Good morning, it’s a pleasure to meet you. I’ve heard a lot about EY, and I’m interested to see how you could potentially help us here at Luse Holdings. 

Alex Thompson (EY Consultant): Good morning, Steve! I’m Alex Thompson, a Senior Manager in Tax at EY, specializing in working with private companies. I’m really excited to be here and learn more about Luse Holdings. I believe we have a variety of services that could be beneficial for you, but first, I’d love to understand more about the specific challenges you're facing. 

Steve Luse: Thank you, Alex. There’s certainly a lot on my plate right now, and I’m keen to explore all avenues of support. 

Alex: That's great to hear, Steve. To kick things off, I’m keen to understand more about the current landscape at Luse Holdings. Are there any specific challenges or areas of the business that are top of mind for you right now?

Steve Luse (CEO): Well Alex, one of the main challenges we’re grappling with is the increasing competition from non-union contractors in our industry. It’s really shaking things up and forcing us to reconsider our traditional business model. We lost a key bid to a non-union contractor recently, and it’s been a wake-up call for us.

Alex Thompson (EY Consultant): I see, that sounds like a significant challenge. The shift towards non-union contractors has indeed been a trend in the industry. Can you share more about how this is specifically impacting Luse Holdings, and what strategies you're considering to navigate these changes?

Steve Luse: Absolutely, Alex. The most immediate impact has been on our pricing. We simply can't compete with non-union contractors on price, and it's putting a lot of pressure on our margins. We're considering several strategies at the moment. One option is to reevaluate our cost structure and see where we can make efficiencies. Another is to potentially explore transitioning to a non-union model ourselves, though that comes with its own set of challenges, particularly around how it might affect our company culture and values.

Alex Thompson: Those are significant considerations, Steve. Making efficiencies within the current cost structure can be a viable option, and exploring a transition needs careful thought, particularly when it comes to preserving the company's values and culture. Have you thought about how you might navigate the potential transition to a non-union model while maintaining the aspects of your culture that are important to Luse Holdings?

Steve Luse: It’s a tough question, Alex. Our employees and the culture we've built here are incredibly important to us. We’re proud of being a family-run business and the values that come with that. Any transition would need to be handled very carefully to ensure we don’t lose what makes Luse Holdings special. 

Alex Thompson: That’s a really important point, Steve. Preserving the unique aspects of Luse Holdings while navigating these market changes will be key. In our experience at EY working with family-run businesses going through similar transitions, a clear and well-communicated strategy, along with employee engagement, can play a crucial role in maintaining company culture. Additionally, considering the potential tax implications and financial structuring in advance can help smooth the transition. We could potentially work together to create a strategic plan that aligns with Luse Holdings' values and helps navigate these changes. Would that be something you’d be interested in exploring further?

Steve Luse: That does sound like a potentially helpful avenue, Alex. I’m open to exploring all options that could help us navigate these challenging times while preserving what makes Luse Holdings unique. Let’s discuss this further and see how EY could support us in creating a strategic plan that aligns with our values and goals.

Alex Thompson (EY Consultant): Absolutely, Steve. I'm glad to hear that you're open to exploring different avenues. Our approach at EY is very much aligned with preserving the unique attributes of family-run businesses like Luse Holdings, while helping to navigate the complexities of the current market.

Steve Luse: That’s reassuring to hear, Alex. So, how do we start? What’s the next step in exploring this strategic planning with EY?

Alex Thompson: The first step would be to conduct a thorough assessment of the current state of Luse Holdings. We would look at your financials, operations, and market positioning to understand where efficiencies can be made and identify potential areas for strategic change. From there, we can work together to develop a roadmap that aligns with your goals and values, while also addressing the challenges posed by the current market conditions.

Steve Luse: That sounds like a comprehensive approach, Alex. I’m interested in understanding how this process would unfold and what kind of timeframe we are looking at.

Alex Thompson: Typically, the initial assessment phase takes around 4-6 weeks, depending on the complexity of the business and the availability of data. After that, we would move into the strategic planning phase, where we start to map out the potential paths forward, evaluate the pros and cons of each, and start to develop a detailed plan. This phase can take anywhere from a few weeks to a few months, again depending on complexity and the depth of analysis required. Throughout the process, we ensure regular check-ins and updates to keep you in the loop and gather your input.

Steve Luse: I appreciate the transparency, Alex. Keeping an open line of communication throughout the process is important to me. I think we’re ready to move forward with this assessment and see what strategic options we can come up with.

Alex Thompson: That’s great to hear, Steve. I’m confident that together we can navigate these challenges and position Luse Holdings for continued success. I’ll coordinate with my team to get the ball rolling on the initial assessment, and we’ll schedule a follow-up meeting to discuss our findings and next steps. In the meantime, if you have any questions or need any additional information, please don’t hesitate to reach out.

Steve Luse: I will do, Alex. Thank you for your time today, and I’m looking forward to seeing what we can achieve together.

Alex Thompson: Thank you, Steve. It's been a pleasure meeting you, and I'm excited about the opportunity to work together. We’ll be in touch soon with next steps, and we're here for any questions in the meantime. Have a great day!

Steve Luse: You too, Alex. Take care.

"""


feedback = """
You are now acting as a client meeting coach. You will only provide constructive feedback on how the consultant behaves during the meeting in a format of JSON String.
    [{
        "Goal": "Quote the goal below",
        "Good behaviors": "[
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history"
        ]",
        "Areas to improve": [
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history"
        ]"
    },
    {
        "Goal": "Quote the goal below",
        "Good behaviors": [
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history"
        ]",
        "Areas to improve": [
            "Feedback rubric 1 with specific examples from the chat history",
            "Feedback rubric 2 with specific examples from the chat history"
        ]"
    }]
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
        ]
    },
    {
        "Goal": "Establish the basis for a successful future business relationship with Steve personally and with Vertex Construction on a corporate level",
        "Good behaviors": [
            "Adjust your social style to that of your client",
            "Demonstrate EQ"
        ],
        "Areas to improve": [
            "Ask close-ended questions",
            "Not showing interest in the client's business"
        ]
    },
    {
        "Goal": "Demonstrate credibility for yourself and for your company",
        "Good behaviors": [
            "Make a good self-introduction that highlights your experience related to client's agenda",
            "Leverage the team behind you: If you don't know the exact of something, make introductions to other points of contact in your company who have relevant expertise"
        ],
        "Areas to improve": [
            "Pretend that you know all the answers",
            "Keep talking past success stories"
        ]
    },
]  
"""


# Get Feedback from GenAI
def get_feedbackai_demo_purpose(request):
    messages = [
        {
            "role": "system",
            "content": chat_history_demo + feedback,  # system message
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    try:
        feedbackai = response.choices[0].message["content"].strip()
        return JsonResponse({"response": feedbackai})
    except openai.error.OpenAIError as e:
        return JsonResponse({"status": "error", "message": str(e)})


# Get Feedback based on your chat history
def get_feedbackai(request):
    # if len(chat_history) < 8:
    #     return JsonResponse({"response": "Please continue the conversation for longer"})
    # else:
    messages = [
        {
            "role": "system",
            "content": json.dumps(chat_history) + feedback,  # system message
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    try:
        feedbackai = response.choices[0].message["content"].strip()
        print("模型回复", feedbackai)
        return JsonResponse({"response": feedbackai})
    except openai.error.OpenAIError as e:
        return JsonResponse({"status": "error", "message": str(e)})


user_message = []
assistant_message = []
chat_history = []


def ask_openai(message):
    system_message_content = SYSTEM_PROMT
    messages = [
        {
            "role": "system",
            "content": system_message_content,  # system message
        },
    ]
    # Add previous conversation to messages
    for um, am in zip(user_message, assistant_message):
        messages.append({"role": "user", "content": um})
        messages.append({"role": "assistant", "content": am})

    # Append the new user message
    messages.append({"role": "user", "content": message})

    chat_history.append({"You-Consultant": message})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    print("刚刚喂进去了什么", messages)
    try:
        answer = response.choices[0].message["content"].strip()
        messages.append({"role": "assistant", "content": answer})
        chat_history.append({"Steve-Client CEO": answer})
        return answer
    except openai.error.OpenAIError as e:
        return str(e)


def chatbot(request):
    chats = Chat.objects.all()

    if request.method == "POST":
        # message is user input
        message = request.POST.get("message")
        # response is one line
        response = ask_openai(message)
        user_message.append(message)
        print("我说了啥", user_message)
        print("Steve说了啥", assistant_message)
        assistant_message.append(response)
        chat = Chat(
            message=message,
            response=response,
            created_at=timezone.now,
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})


def simulationlab(request):
    return render(request, "simulationlab.html")
