import tkinter as tk
import speech_recognition as sr

def save_speech_to_text():
    global run
    run = True
    r = sr.Recognizer()
    r.pause_threshold = 3
    i = 0
    while run:

        print(i)
        i = i + 1
        with sr.Microphone() as source:
            status_label.config(text="Rozpocznij mówienie...")
            root.update()
            audio = r.listen(source, timeout=None, phrase_time_limit=50)
            status_label.config(text="Zakończono nagrywanie.")
            root.update()
        try:
            text = r.recognize_google(audio, language='pl-PL')
            if "koniec nagrywania" in text:
                print("Koniec nagrywania.")
                break
            with open("speech_to_text.txt", "a", encoding="UTF-8") as file:
                file.write(text + "\n")
                status_label.config(text="Mowa zapisana w pliku.")
                root.update()
            with open("speech_to_text.txt", "r", encoding="UTF-8") as file:
                word_count = len(file.read().split())
                word_count_label.config(text="Liczba słów w pliku: " + str(word_count))
        except sr.UnknownValueError:
            status_label.config(text="Nie udało się przetworzyć mowy.")
            root.update()
        except sr.RequestError as e:
            status_label.config(text="Błąd połączenia z API Google Cloud Speech Recognition: {0}".format(e))
            root.update()
        except KeyboardInterrupt:
            status_label.config(text="Przerwano nagrywanie")
            root.update()

def stop_recording():
    global run
    run = False
    """
    with open("speech_to_text.txt", "a", encoding="UTF-8") as file:
        file.write("koniec nagrywania\n")
        status_label.config(text="Koniec nagrywania.")
        root.update()
    """
root = tk.Tk()
root.title("Speech to Text")


status_label = tk.Label(root, text="Wciśnij przycisk, aby rozpocząć nagrywanie.")
status_label.pack()

word_count_label = tk.Label(root)
word_count_label.pack()

button = tk.Button(root, text="Rozpocznij nagrywanie", command=save_speech_to_text)
button.pack()

stop_button = tk.Button(root, text="Zakończ nagrywanie", command=stop_recording)
stop_button.pack()

root.mainloop()