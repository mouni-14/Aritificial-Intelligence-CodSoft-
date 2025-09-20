from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Predefined responses
responses = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! What can I do for you?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "what is your name": "I am MiniBot, your friendly chatbot.",
    "bye": "Goodbye! Have a nice day.",
}

def get_response(message):
    message = message.lower()
    for key in responses:
        if key in message:
            return responses[key]
    return "Sorry, I don't understand. Can you rephrase?"

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    bot_reply = get_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
