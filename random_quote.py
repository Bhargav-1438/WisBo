import random

def run(arg=""):
    quotes = [
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Success is not in what you have, but who you are. – Bo Bennett",
        "Dream big and dare to fail. – Norman Vaughan",
        "Don’t watch the clock; do what it does. Keep going. – Sam Levenson"
    ]
    return f"💡 Quote of the Moment:\n{random.choice(quotes)}"
