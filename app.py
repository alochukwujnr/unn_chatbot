from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Load data from JSON files
with open("unn_data/departments.json") as d:
    departments = json.load(d)

with open("unn_data/locations.json") as l:
    locations = json.load(l)


@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Check for department information
    for dept, info in departments.items():
        if dept.lower() in incoming_msg:
            msg.body(f"{dept} Department 🏫\nHOD: {info['HOD']}\nOffice: {info['Office']}")
            return str(resp)

    # Check for location information
    for place, desc in locations.items():
        if place.lower() in incoming_msg:
            msg.body(f"{place} 📍\n{desc}")
            return str(resp)

    # Default / fallback response
    msg.body(
        "Hi 👋 I’m the UNN Campus Guide Chatbot.\n"
        "You can ask me things like:\n"
        "• Where is the ICT Building?\n"
        "• Who is the HOD of Computer Science?\n"
        "• Where is the Student Affairs Office?"
    )
    return str(resp)


if __name__ == "__main__":
    app.run(port=5000)
