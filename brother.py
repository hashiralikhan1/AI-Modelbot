
from datetime import datetime

def brother(message):
    message = message.lower().strip()

    if message in ["hello", "hi", "salam"]:
        return "Assalam-o-Alaikum bhai! Main BROTHER hoon."

    if "time" in message:
        return datetime.now().strftime("Abhi time %I:%M %p hai.")

    if "date" in message:
        return datetime.now().strftime("Aaj %d %B %Y hai.")

    return "Bhai, main abhi seekh raha hoon. Jald AI features add honge."

print("BROTHER AI is running!")
print("Band karne ke liye exit likho.")

while True:
    message = input("\nYou: ")

    if message.lower().strip() == "exit":
        print("BROTHER: Allah Hafiz!")
        break

    print("BROTHER:", brother(message))
