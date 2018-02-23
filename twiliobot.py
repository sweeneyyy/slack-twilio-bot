import os
from flask import Flask, request, Response, jsonify, abort
from slackclient import SlackClient 
from twilio import twiml
# from twilio.twiml.messaging_response import Message, MessagingResponse 
from twilio.rest import TwilioRestClient
from textblob import TextBlob


SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
USER_NUMBER = os.environ.get('USER_NUMBER', None)

app = Flask(__name__)

slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
twilio_client = TwilioRestClient()

# post route for sms msg from twilio to slack channel
@app.route('/twilio', methods=['POST'])
def twilio_post():
  response = twiml.Response()
  # response = MessagingResponse()
  # print('Msgresponse', response)

  if request.form['From'] == USER_NUMBER:
    message = request.form['Body']
    slack_client.api_call("chat.postMessage", channel="#general", 
                          text=message, username='twiliobot', 
                          icon_emoji=':robot_face:')
  return Response(response, mimetype="text/xml"), 200

# post route for sms msg from slack channel to phone
@app.route('/slack', methods=['POST'])
def slack_post():
  if request.form['token'] == SLACK_WEBHOOK_SECRET:
    channel = request.form['channel_name']
    username = request.form['user_name']
    text = request.form['text']
    response_message = username + " in " + channel + " says: " + text
    twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
                                  body=response_message,
                                  media_url="https://www.twilio.com/blog/wp-content/uploads/2016/05/ZBxjTSYSCXtvdxKG77UqOmQ7r4iFqGJIe1LrmTSC2Z5kKUJalpzZqp5Fmk-6DVJKpyTjWmiFxhTZT4ltsR8uHSkAYd2gcrszkz3o7QZ3ck0yghh2jkrta1P1nVoEKW5781fZjn2o.png")

  return Response(), 200

# testing slash command
@app.route('/hello', methods=['POST'])
def hello():
  return 'Hello Slack!'

# translate slash command
@app.route('/translate', methods=['POST'])
def translate():
  # token = request.form.get('SLACK_TOKEN', None)
  command = request.form.get('/translate', None)
  text = request.form.get('text', None)
  # if not token:
  #   abort(400)
  is_translated = TextBlob(text).translate(to='es')
  print(is_translated)

  return jsonify({
    'response_type': 'in_channel',
    'text': str(is_translated),
  })

# see cute puppies slash command
@app.route('/puppies', methods=['POST'])
def puppies():
  command = request.form.get('/puppies', None)
  text = request.form.get('text', None)

  return jsonify({
    'response_type': 'in_channel',
    'text': 'puppies!',
    'attachments': [
      { 
        'image_url': 'https://steemitimages.com/DQmNgA63knJTBE5gUUYxC9UUiWrUHKMP2dx1qeKiR88696Q/cute-dogs-and-puppies-wallpaper-2.jpg'
      }
    ] 
  })


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)


