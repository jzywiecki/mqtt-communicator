import tkinter as tk
import paho.mqtt.client as mqtt
import speech_recognition as sr
import pyttsx3
import sys


def on_message(client, userdata, message):
    '''
    Funkcja obsługująca otrzymane wiadomości.
    W przypadku kiedy wiadomości nie są wyciszone wiadomość jest wyswietlona w messages_display i wypowiedziana
    za pomocą TTS. Inaczej dodajemy ją do listy "messages".
    '''
    print("Zarejestrowano wiadomosc!")
    if not muted:
        messages_display.config(state="normal")
        messages_display.insert("end", f"{message.payload.decode()} ({message.topic})\n")
        messages_display.see("end")
        messages_display.config(state="disabled")
        engine = pyttsx3.init()
        engine.say(message.payload.decode())
        engine.runAndWait()
    else:
        show_button.configure(bg='green')
        messages.append((message.payload.decode(), message.topic))

def send_message():
    '''
    Funkcja wysyłająca wiadomość na temat "msg/mic".
    Tekst składa się z wprowadzonej nazwy użytkownika oraz wiadomości.
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    text = r.recognize_google(audio, language="pl-PL")
    text = name + " mówi " + text

    publishing = sys.argv[3]
    print(publishing)
    client.publish(publishing, text)


def toggle_mute():
    '''
    Funkcja włączająca i wyłączająca tryb wyciszenia.
    W obu przypadkach w message_display pojawia się stosowana informacja i zmienia się napis na przycisku.
    '''
    global muted
    if muted:
        muted = False
        mute_button.config(text="Wycisz odtwarzanie")
        messages_display.config(state="normal")
        messages_display.insert("end", "Włączono odtwarzanie.\n")
        messages_display.config(state="disabled")
    else:
        muted = True
        mute_button.config(text="Odtwarzaj wiadomości")
        messages_display.config(state="normal")
        messages_display.insert("end", "Wyciszono odtwarzanie.\n")
        messages_display.see("end")
        messages_display.config(state="disabled")

def play_messages():
    '''
    Funkcja wypowiadająca wiadomości z listy messages.
    '''
    for message, topic in messages:
        engine.say(message)
        engine.runAndWait()
    messages.clear()


def show_messages():
    '''
    Funkcja wyświetlająca nieodczytane wiadomości, w przypadku gdy wiadomości są najpierw wypisujemy je w polu
    messages_display, a następnie odczytujemy je na głos używając TTS
    '''
    if messages:
        defaultcolor=root.cget('bg')
        show_button.configure(bg=defaultcolor)
        messages_display.config(state="normal")
        messages_display.insert("end", "Nieodczytane wiadomości:\n")
        for message, topic in messages:
            messages_display.insert("end", f"{message} ({topic})\n")
        messages_display.see("end")
        messages_display.config(state="disabled")
        root.after(20, play_messages)
    else:
        messages_display.config(state="normal")
        messages_display.insert("end", "Brak nieodczytanych wiadomości.\n")
        messages_display.see("end")
        messages_display.config(state="disabled")

if __name__ == '__main__':
    # inicjalizacja klienta MQTT
    client = mqtt.Client()

    # inicjalizacja interfejsu
    root = tk.Tk()
    root.title("Aplikacja MQTT")

    #inicjacja TTS
    engine = pyttsx3.init()

    #wyciagniecie nazwy uzytkownika
    name = sys.argv[1]

    # przycisk wysyłający wiadomość
    send_button = tk.Button(root, text="Wyślij", command=send_message)
    send_button.pack()

    # pole tekstowe z wiadomościami
    messages_display = tk.Text(root, height=10, state="disabled")
    messages_display.pack()

    # przycisk wyciszający i odciszający odtwarzanie wiadomości
    mute_button = tk.Button(root, text="Wycisz odtwarzanie", command=toggle_mute)
    mute_button.pack()

    # przycisk wyświetlający nieodczytane wiadomości
    show_button = tk.Button(root, text="Pokaż nieodczytane wiadomości", command=show_messages)
    show_button.pack()

    # przycisk zamykający aplikację
    exit_button = tk.Button(root, text="Zamknij", command=root.quit)
    exit_button.pack()

    # konfiguracja klienta MQTT
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883)

    recieving = sys.argv[2]
    print(recieving)
    client.subscribe(recieving)
    client.loop_start()

    # lista przechowująca nieodczytane wiadomości
    messages = []
    # flaga określająca, czy tryb wyciszenia jest włączony
    muted = False

    # główna pętla programu
    root.mainloop()