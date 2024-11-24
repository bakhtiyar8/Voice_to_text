# Voice_to_text
Explanation of the Code and Installation Instructions:
import os
import wave
import json
import pyaudio
import sqlite3
import language_tool_python
from vosk import Model, KaldiRecognizer
from tkinter import Tk, Button, Label, Text, END, OptionMenu, StringVar, IntVar, filedialog, ttk
from threading import Thread
from queue import Queue
from datetime import datetime

Standard Libraries: os, wave, json, datetime (for file paths, audio manipulation, JSON parsing, timestamps)
Third-Party Libraries:
pyaudio: For recording audio from the microphone (install: pip install pyaudio)
sqlite3: For storing transcription results in a database (included in Python)
language_tool_python: For optional grammar correction (install: pip install languagetool-python)
vosk: For speech recognition using Vosk models (install: pip install vosk)
tkinter: For creating the graphical user interface (GUI) (included in Python)
threading: For running recording as a separate thread

2. Database Initialization:
 # Initialize the database
conn = sqlite3.connect('transcriptions.db')
c = conn.cursor()

Connects to a SQLite database named transcriptions.db and creates a cursor to interact with it.

3. Vosk Model Paths:

# Initialize Vosk models
model_paths = {
    'English': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-en-us-0.15',
    'Chinese': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-cn-0.22',
    'Uzbek': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-uz-0.22',
    'Russian': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-ru-0.22'
}

models = {lang: Model(path) for lang, path in model_paths.items()}

I'd be glad to create a comprehensive response combining the strengths of Response A and Response B, addressing their shortcomings, and incorporating insights from the ratings:

Explanation of the Code and Installation Instructions:

1. Imports:

Python
import os
import wave
import json
import pyaudio
import sqlite3
import language_tool_python
from vosk import Model, KaldiRecognizer
from tkinter import Tk, Button, Label, Text, END, OptionMenu, StringVar, IntVar, filedialog, ttk
from threading import Thread
from queue import Queue
from datetime import datetime
Используйте код с осторожностью.

Standard Libraries: os, wave, json, datetime (for file paths, audio manipulation, JSON parsing, timestamps)
Third-Party Libraries:
pyaudio: For recording audio from the microphone (install: pip install pyaudio)
sqlite3: For storing transcription results in a database (included in Python)
language_tool_python: For optional grammar correction (install: pip install languagetool-python)
vosk: For speech recognition using Vosk models (install: pip install vosk)
tkinter: For creating the graphical user interface (GUI) (included in Python)
threading: For running recording as a separate thread
2. Database Initialization:

Python
# Initialize the database
conn = sqlite3.connect('transcriptions.db')
c = conn.cursor()
Используйте код с осторожностью.

Connects to a SQLite database named transcriptions.db and creates a cursor to interact with it.

3. Vosk Model Paths:

Python
# Initialize Vosk models
model_paths = {
    'English': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-en-us-0.15',
    'Chinese': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-cn-0.22',
    'Uzbek': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-uz-0.22',
    'Russian': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-ru-0.22'
}

models = {lang: Model(path) for lang, path in model_paths.items()}
Используйте код с осторожностью.

Defines a dictionary model_paths to store the paths to Vosk speech recognition models for different languages.
Creates a dictionary models that maps language names to loaded Vosk models.
Important: Replace the example paths with the actual locations of your downloaded Vosk models. Download them from the Vosk website (https://alphacephei.com/vosk/).
4. LanguageTool Initialization (Optional):

# Initialize LanguageTool for grammar correction
tools = {
    'English': language_tool_python.LanguageTool('en-US'),
    'Chinese': language_tool_python.LanguageTool('zh-CN'),
    'Russian': language_tool_python.LanguageTool('ru')
}


Defines a dictionary tools to store instances of LanguageTool for grammar correction in supported languages.
Important: This section is optional. If you want grammar correction, install languagetool-python and replace language codes with supported ones.
5. Queue for Database Operations:


# Queue for database operations
db_queue = Queue()


Creates a queue (db_queue) to handle database operations asynchronously from the main GUI thread.

6. Recording and Transcription Functions:

recording = False  # Initialize the recording variable
table_name = None  # Initialize the table_name variable

def record_audio(filename, duration=30):
    # ... (code for recording audio) ...

def transcribe_audio(filename, language):
    # ... (code for transcribing audio using Vosk) ...

def correct_grammar(text, language):
    # ... (code for grammar correction using LanguageTool) ...



I'd be glad to create a comprehensive response combining the strengths of Response A and Response B, addressing their shortcomings, and incorporating insights from the ratings:

Explanation of the Code and Installation Instructions:

1. Imports:

Python
import os
import wave
import json
import pyaudio
import sqlite3
import language_tool_python
from vosk import Model, KaldiRecognizer
from tkinter import Tk, Button, Label, Text, END, OptionMenu, StringVar, IntVar, filedialog, ttk
from threading import Thread
from queue import Queue
from datetime import datetime
Используйте код с осторожностью.

Standard Libraries: os, wave, json, datetime (for file paths, audio manipulation, JSON parsing, timestamps)
Third-Party Libraries:
pyaudio: For recording audio from the microphone (install: pip install pyaudio)
sqlite3: For storing transcription results in a database (included in Python)
language_tool_python: For optional grammar correction (install: pip install languagetool-python)
vosk: For speech recognition using Vosk models (install: pip install vosk)
tkinter: For creating the graphical user interface (GUI) (included in Python)
threading: For running recording as a separate thread
2. Database Initialization:

Python
# Initialize the database
conn = sqlite3.connect('transcriptions.db')
c = conn.cursor()
Используйте код с осторожностью.

Connects to a SQLite database named transcriptions.db and creates a cursor to interact with it.

3. Vosk Model Paths:

Python
# Initialize Vosk models
model_paths = {
    'English': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-en-us-0.15',
    'Chinese': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-cn-0.22',
    'Uzbek': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-uz-0.22',
    'Russian': 'C:\\Users\\Bakhtiyar\\Desktop\\Python\\Meeting_notes\\vosk-model-small-ru-0.22'
}

models = {lang: Model(path) for lang, path in model_paths.items()}
Используйте код с осторожностью.

Defines a dictionary model_paths to store the paths to Vosk speech recognition models for different languages.
Creates a dictionary models that maps language names to loaded Vosk models.
Important: Replace the example paths with the actual locations of your downloaded Vosk models. Download them from the Vosk website (https://alphacephei.com/vosk/).
4. LanguageTool Initialization (Optional):

Python
# Initialize LanguageTool for grammar correction
tools = {
    'English': language_tool_python.LanguageTool('en-US'),
    'Chinese': language_tool_python.LanguageTool('zh-CN'),
    'Russian': language_tool_python.LanguageTool('ru')
}
Используйте код с осторожностью.

Defines a dictionary tools to store instances of LanguageTool for grammar correction in supported languages.
Important: This section is optional. If you want grammar correction, install languagetool-python and replace language codes with supported ones.
5. Queue for Database Operations:

Python
# Queue for database operations
db_queue = Queue()
Используйте код с осторожностью.

Creates a queue (db_queue) to handle database operations asynchronously from the main GUI thread.

6. Recording and Transcription Functions:

Python
recording = False  # Initialize the recording variable
table_name = None  # Initialize the table_name variable

def record_audio(filename, duration=30):
    # ... (code for recording audio) ...

def transcribe_audio(filename, language):
    # ... (code for transcribing audio using Vosk) ...

def correct_grammar(text, language):
    # ... (code for grammar correction using LanguageTool) ...
Используйте код с осторожностью.

These functions encapsulate the core functionalities:

record_audio: Records audio from the microphone for a specified duration (default: 30 seconds).
transcribe_audio: Transcribes the audio from the given filename using the selected Vosk model.
correct_grammar (optional): Corrects grammar in the transcribed text using LanguageTool if available for the selected language.
7. Database Interaction:
def save_to_


All can be found in file record_audio_8_db.py

Please use record_audio_9_db.spec file to create .exe file.

Thank you for attantion and using code!
