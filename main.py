import eventlet
# IMPORTANT: monkey_patch before any other imports
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# In-memory stores for transcripts & summaries
transcript_store = {}  # video_id -> full transcript text
summary_store = {}     # video_id -> latest markdown summary

@app.route('/')
def index():
    return render_template('index.html')


def strip_audio(video_path):
    """
    Stub: extract audio track from video.
    Returns path to audio file (e.g., WAV/MP3).
    """
    # TODO: use pydub or ffmpeg-python
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    return audio_path


def transcribe_audio(audio_path):
    """
    Stub: stream speech-to-text.
    Yields chunks of transcript as they become available.
    """
    sample_chunks = [
        "In this lesson, we explore the fundamentals of differential calculus.",
        "The derivative quantifies the rate of change of a function with respect to its variable.",
        "We demonstrate the limit definition: as h approaches zero, (f(x+h)-f(x))/h.",
        "For example, if f(x) = x^2, then f'(x) = 2x.",
        "Next, we consider applications of the derivative in physics, such as velocity and acceleration.",
    ]
    for chunk in sample_chunks:
        time.sleep(3)
        yield chunk


def generate_summary(text):
    """
    Stub: generate a Markdown summary from full transcript so far.
    Returns a rich demonstration summary.
    """
    # Rich demonstration markdown summary
    summary = '''
### Calculus: Derivatives & Integrals

**1. The Derivative**  
- **Definition**: The derivative measures the instantaneous rate of change of a function.  
- **Notation**: `f'(x)`, `d/dx f(x)`  
- **Limit Definition**:  
```
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
```

**2. Key Examples**  
- If `f(x) = x^2`, then `f'(x) = 2x`.  
- The derivative of `sin(x)` is `cos(x)`.

---

### Integration

**1. The Integral**  
- **Definition**: The integral accumulates the area under a curve.  
- **Notation**: `\int f(x) dx`  

**2. Fundamental Theorem of Calculus**  
> The integral of a derivative over an interval yields the original function's net change:
```
\int_a^b f'(x) dx = f(b) - f(a)
```

*This summary is updated in real-time as the lesson progresses.*
'''    
    return summary


def update_summary_loop():
    """
    Background thread: for a given video file,
    strip audio -> transcribe -> update summary_store & emit updates.
    """
    video_id = 'sample_lesson'
    video_path = 'static/sample_lesson.mp4'
    # 1. Extract audio
    audio_path = strip_audio(video_path)
    # 2. Transcribe in chunks
    transcript = ''
    transcript_store[video_id] = transcript
    for chunk in transcribe_audio(audio_path):
        transcript += '\n' + chunk
        transcript_store[video_id] = transcript
        # 3. Generate & store updated summary
        summary = generate_summary(transcript)
        summary_store[video_id] = summary
        # 4. Emit Markdown summary to clients
        socketio.emit('summary_update', {'summary': summary})

@socketio.on('connect')
def on_connect():
    # On new connection, send latest summary if available
    video_id = 'sample_lesson'
    summary = summary_store.get(
        video_id,
        "## Live Summary\n\nWaiting for transcription..."
    )
    emit('summary_update', {'summary': summary})


def answer_question(question):
    """
    Stub: answer user question in Markdown.
    Distinguish between STT-based and internet-based answers.
    """
    # Use STT context for a concise answer
    stt_part = f"**Answer from STT Summary:**  \nBased on the lesson transcript, here's a focused answer to your question: *{question}*\n\n"
    internet_part = "**Answer from Internet:**  \nThis section provides additional context or examples sourced from online resources."
    return stt_part + internet_part

@socketio.on('chat_message')
def handle_chat(data):
    question = data.get('question', '').strip()
    if not question:
        return
    answer = answer_question(question)
    emit('chat_response', {'question': question, 'answer': answer}, broadcast=True)

if __name__ == '__main__':
    # Start the summary thread in daemon mode
    threading.Thread(target=update_summary_loop, daemon=True).start()
    socketio.run(app, debug=True)
