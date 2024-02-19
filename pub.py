# Digital Pub v1.0
#
#TODO: direct back to previous guest when sentence contains "?" because it could be follow-up question..
#TODO: exhaust score for discussion. end discussion when response starts with: Thank you or contains "You're absolutely right" or "That's correct" or "You are correct"

import sys
import random
import argparse
from openai import OpenAI

# Create the parser
parser = argparse.ArgumentParser(description="Run a Digital Pub")
parser.add_argument('--topic', type=str, help='Topic of the day or question for pub quiz.', required=True)
parser.add_argument('--type', type=str, choices=['quiz', 'talk'], help='Can be either quiz or talk. In quiz mode, each robot gives one response before the program ends. Talk mode will be endless until you stop by pressing Ctrl+C.', default="talk")
args = parser.parse_args()

BASE_URL = "http://localhost:1234/v1"
TOPIC_OF_THE_DAY = args.topic

# Pub customers
pub = {
    "Hans": {
        "role": "system",
        "content": "You are a critical chat partner. You respond in short and precise sentences. You can be sarcastic or humorous. You never repeat yourself.",
        "temperature": 0.3
    },
    "Robert": {
        "role": "system",
        "content": "You love to challenge everything that is said. Be an agressive but friendly chat partner. Your answers are very short but concise. You never repeat yourself.",
        "temperature": 0.5
    },
    "GrumpyMax": {
        "role": "system",
        "content": "You only see the negative and are a very pessimistic character. You are an old retired steel worker. You love to tease your interlocutor to provoke a reaction. You never repeat yourself.",
        "temperature": 0.7
    },
    "MrsSunshine": {
        "role": "system",
        "content": "You are a true sunshine filled with positivity and happiness. You are a teenage girl. You hate discussing negative topics but you try to understand and find a positive aspect in what is being said. You never repeat yourself. You love animals and nature!",
        "temperature": 0.7
    },
    "Carl": {
        "role": "system",
        "content": "You are a slick genious and always come up with a solution for everything. You have an opinion on everything. You try to always look at a topic from the negative and the positive side. You never repeat yourself.",
        "temperature": 0.2
    },
    "ThatTravelGuy": {
        "role": "system",
        "content": "You know everything about every country and city in the world. You love to share your experiences from all the places you have visited. You give detailed answers when the topic is travel or vacation related but your answers are short otherwise. You never repeat yourself.",
        "temperature": 0.8
    }
}

people = list(pub.keys())

def get_random_guest(pub: dict) -> str:
    return random.choice(list(pub.keys()))


def main():
    # Create chat client for each person in the pub.
    clients = {}
    for person in pub.keys():
        clients[person] = {
            "session": OpenAI(base_url=BASE_URL, api_key="not-needed"),
            "init": True
        }

    global_history = [
        {"role": "user", "content": TOPIC_OF_THE_DAY}
    ]

    print("# ChatBot Digital Pub v1.0")
    print(f"## {global_history[-1]['content']}")
    print(f"**{args.type.upper()}** Mode")
    print("\n### Guests")
    for person in pub.keys():
        print(f"* {person}")
    print("-"*23)

    last_speaker = ""
    print("### Talk")
    while True:
        if args.type == "talk":
            # Pick a random pub member but not the last one speaking.
            while True:
                guest = get_random_guest(pub)
                if guest != last_speaker:
                    last_speaker = guest
                    break
        elif args.type == "quiz":
            try:
                guest = people.pop(0)
            except Exception as e:
                print(str(e))
                sys.exit(0)

        print(f"\n#### {guest}")
        if clients[guest].get('init'):
            history = [pub.get(guest,[])] + global_history
            clients[guest]['init'] = False
        else:
            history = global_history

        # Setup client.
        client = clients[guest]['session']
        completion = client.chat.completions.create(
            model="local-model", # this field is currently unused.
            messages=history,
            temperature=clients[guest].get('temperature',0.7),
            stream=True,
            user=guest
        )
        message = {
            "role": "user",
            "content": ""
        }

        # Chat completion
        for chunk in completion:
            partial_answer = chunk.choices[0].delta.content
            if partial_answer:
                print(partial_answer, end="", flush=True)
                message["content"] += partial_answer

        if not message['content']:
            sys.exit(1)
        if args.type == "talk":
            global_history.append(message)
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n\n> **EXIT**\n> You got kicked out of the pub...\n")
