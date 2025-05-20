# CoTeacher MVP – Flask + Socket.IO

This web-based application is an MVP for CoTeacher — a tool that lets users:  
- Select and play a local video lesson  
- View live AI-generated summaries of the video  
- Chat with an AI assistant trained on the video content  

## Project Structure

```text
/python_flask_test/
├── main.py                  # Main Flask + SocketIO backend
├── templates/
│   ├── index.html           # UI layout: summary, video, chat
│   └── readme.html          # This README file
└── static/
    └── sample_lesson.mp4    # Optional sample video file
```

## Features Implemented

* Live summary updates via `SocketIO` from backend to frontend
* Chat interface where users can ask questions; answers are generated on server side
* All dynamic communication handled in real time via WebSockets

## What I Used

* **Python 3.10+**
* **Flask** – for web server
* **Flask-SocketIO** – for real-time communication
* **Eventlet** – async WebSocket backend
* **HTML/JS (browser)** – frontend UI

## Installation

### 1. Install Python packages

```bash
pip install flask flask-socketio eventlet
```

### 2. File layout requirement

Place your HTML template in a folder named `templates/`, and any videos or assets in `static/`.

### 3. Start the application

```bash
python main.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Important Notes

* `eventlet.monkey_patch()` must appear at the very top of `main.py`, before any other imports.
* The summary stream in this version is simulated. Later you can hook it into Whisper or real-time transcription.
* The chat bot response is placeholder text. Later you can integrate with OpenAI GPT or another LLM.

## Next Steps

* Handle video file upload, strip audio and perform STT
* Send transcript to OpenAI API for live summary
* Send chat context including transcript to OpenAI API smart chat responses
