# mqtt-communicator

The Simple Communicator using MQTT protocol is a program that allows users to communicate with each other using their voice. The program uses the MQTT protocol, a lightweight messaging protocol, to transmit messages between clients.

To send a message, the user speaks into their microphone, and the program uses a Speech-to-Text engine to convert their speech into text. The text message is then sent over MQTT to the intended recipient.

To receive a message, the program listens for incoming messages over MQTT. When a new message is received, the program uses a Text-to-Speech engine to convert the message from text to speech, which is then played back to the user. The message is also displayed on the user's screen for visual reference.

The program is designed to be simple and easy to use. Users can choose their own MQTT broker and topic to communicate on, and can easily switch between sending and receiving messages.

## Usage:
python communicator.py name topic-to-send topic-to-recieve

## Main screen
![image](https://user-images.githubusercontent.com/105950890/231313123-3f9fbc08-061d-4f37-8eff-c606e2ed7e76.png)

## Multiple users
We can use multiple users to communicate on different topics
![image](https://user-images.githubusercontent.com/105950890/231313142-45cf1cb6-4c06-493c-93d3-0dd5f1d5cc7b.png)

## Silence mode
User can enter silence mode - messages will wait for user to recieve them
![image](https://user-images.githubusercontent.com/105950890/231313151-43a74927-352b-4524-a7a0-27ebf168033b.png)

## Gathering messages in silence mode
Awaiting messages are signalised by green button color
![image](https://user-images.githubusercontent.com/105950890/231313168-c802810c-939a-4c4b-869c-62947726477c.png)

## Printing and saying messages using TTS
![image](https://user-images.githubusercontent.com/105950890/231313176-68176fa5-2bd2-431a-9f26-e204ec51c2f9.png)
