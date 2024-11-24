import os
import wave
import json
import pyaudio
import sqlite3
import language_tool_python
from vosk import Model, KaldiRecognizer
from tkinter import Tk, Button, Label, Text, END, OptionMenu, StringVar, IntVar, filedialog, ttk
from tkinter.constants import N, S, E, W
from threading import Thread
from queue import Queue
from datetime import datetime

# Initialize the database
conn = sqlite3.connect('transcriptions.db')
c = conn.cursor()

# Initialize Vosk models
model_paths = {
    'English': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-en-us-0.15',
    'Chinese': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-cn-0.22',
    'Uzbek': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-uz-0.22',
    'Russian': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-ru-0.22'
}
models = {lang: Model(path) for lang, path in model_paths.items()}

# Initialize LanguageTool for grammar correction
tools = {
    'English': language_tool_python.LanguageTool('en-US'),
    'Chinese': language_tool_python.LanguageTool('zh-CN'),
    'Russian': language_tool_python.LanguageTool('ru')
}

# Queue for database operations
db_queue = Queue()

recording = False  # Initialize the recording variable
table_name = None  # Initialize the table_name variable

def record_audio(filename, duration=30):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []

    print("Recording...")
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wave_file.setframerate(16000)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

def transcribe_audio(filename, language):
    wf = wave.open(filename, "rb")
    rec = KaldiRecognizer(models[language], wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))

    results.append(json.loads(rec.FinalResult()))
    wf.close()

    transcripts = [result['text'] for result in results if 'text' in result]
    return ' '.join(transcripts)

def correct_grammar(text, language):
    if language in tools:
        matches = tools[language].check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        return corrected_text
    return text  # Return the original text if grammar correction is not supported

def save_to_database(table_name, text, timestamp, language):
    db_queue.put((table_name, text, timestamp, language))

def update_text_display(table_name):
    c.execute(f"SELECT text, timestamp, language FROM {table_name} ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if row:
        text_display.insert(END, f"{row[1]}: {row[0]} ({row[2]})\n")
        text_display.see(END)  # Scroll to the end

def process_db_queue():
    while not db_queue.empty():
        table_name, text, timestamp, language = db_queue.get()
        if text is None and timestamp is None:
            c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, text TEXT, timestamp TEXT, language TEXT)''')
        else:
            c.execute(f"INSERT INTO {table_name} (text, timestamp, language) VALUES (?, ?, ?)", (text, timestamp, language))
        conn.commit()
        update_text_display(table_name)

def start_recording():
    global recording, table_name
    recording = True
    count = 0
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_name = f"transcriptions_{timestamp}"
    db_queue.put((table_name, None, None, None))  # Signal to create a new table
    root.after(100, process_db_queue)
    notification_label.config(text="Recording started...")
    while recording:
        filename = f'output_{count}.wav'
        record_audio(filename, duration_var.get())
        text = transcribe_audio(filename, selected_language.get())
        corrected_text = correct_grammar(text, selected_language.get())
        timestamp = datetime.now().strftime("%H:%M:%S")
        save_to_database(table_name, corrected_text, timestamp, selected_language.get())
        root.after(100, process_db_queue)
        count += 1
    notification_label.config(text="Recording stopped.")

def stop_recording():
    global recording
    recording = False

def extract_to_document():
    if table_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        document_name = f'meeting_summary_{timestamp}.txt'
        c.execute(f"SELECT text, timestamp, language FROM {table_name}")
        rows = c.fetchall()
        with open(document_name, 'w') as file:
            file.write("Meeting Summary:\n")
            for row in rows:
                file.write(f"{row[1]}: {row[0]} ({row[2]})\n")
        notification_label.config(text=f"Document extracted: {document_name}")

def on_closing():
    global recording
    if recording:
        stop_recording()
    extract_to_document()
    root.destroy()

def select_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
    if file_path:
        global table_name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        table_name = f"transcriptions_{timestamp}"
        db_queue.put((table_name, None, None, None))  # Signal to create a new table
        process_db_queue()
        language = selected_language.get()
        notification_label.config(text="Converting audio file to text...")
        root.update_idletasks()
        text = transcribe_audio(file_path, language)
        corrected_text = correct_grammar(text, language)
        timestamp = datetime.now().strftime("%H:%M:%S")
        save_to_database(table_name, corrected_text, timestamp, language)
        process_db_queue()
        notification_label.config(text="Conversion completed.")

# GUI setup
root = Tk()
root.title("Voice Recorder")

# Use ttk for modern design
style = ttk.Style(root)
style.theme_use('clam')

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(N, S, E, W))

selected_language = StringVar(root)
selected_language.set("English")  # Default value

def update_language_menu(*args):
    menu = language_menu['menu']
    menu.delete(0, 'end')
    for language in model_paths.keys():
        menu.add_command(label=language, command=lambda value=language: selected_language.set(value))

selected_language.trace('w', update_language_menu)

language_label = ttk.Label(main_frame, text="Select Language:")
language_label.grid(row=0, column=0, sticky=W)

language_menu = ttk.OptionMenu(main_frame, selected_language, *model_paths.keys())
language_menu.grid(row=0, column=1, sticky=(W, E))

update_language_menu()  # Initialize the menu with all languages

duration_var = IntVar(root)
duration_var.set(30)  # Default value

duration_label = ttk.Label(main_frame, text="Select Duration (seconds):")
duration_label.grid(row=1, column=0, sticky=W)

duration_menu = ttk.OptionMenu(main_frame, duration_var, 10, 15, 30, 60, 120)
duration_menu.grid(row=1, column=1, sticky=(W, E))

start_button = ttk.Button(main_frame, text="Start Recording", command=lambda: Thread(target=start_recording).start())
start_button.grid(row=2, column=0, sticky=(W, E))

stop_button = ttk.Button(main_frame, text="Stop Recording", command=stop_recording)
stop_button.grid(row=2, column=1, sticky=(W, E))

extract_button = ttk.Button(main_frame, text="Extract to Document", command=extract_to_document)
extract_button.grid(row=3, column=0, sticky=(W, E))

select_file_button = ttk.Button(main_frame, text="Select Audio File", command=select_audio_file)
select_file_button.grid(row=3, column=1, sticky=(W, E))

notification_label = ttk.Label(main_frame, text="")
notification_label.grid(row=4, column=0, columnspan=2, sticky=(W, E))

text_display = Text(main_frame, height=20, width=50)
text_display.grid(row=5, column=0, columnspan=2, sticky=(N, S, E, W))

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

# Close the database connection when the GUI is closed
conn.close()
