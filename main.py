# main.py
import eventlet
eventlet.monkey_patch()  # must come first

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import threading, time, csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# ─── FIX: Declare transcript_store up here ────────────────────────────────
transcript_store = {
    'sample_lesson': []   # will hold { 'time': float, 'text': str } entries
}

# Paste this into your main.py as the new summary_data
SUMMARY_DATA = [
    {
        "timestamp": "0:00",
        "summary": "The lecture introduces the topic of the **definite integral**, asking students to ignore previous associations with the integral symbol ('snakes'), as this approach will feel unrelated at first."
    },
    {
        "timestamp": "0:39",
        "summary": "We pose the key question: What is the **area under the graph** of a function $f$ over the interval $[a, b]$? The assumption is that $f$ is positive and continuous for simplicity, but must be **bounded**."
    },
    {
        "timestamp": "1:52",
        "summary": "Boundedness ensures the function doesn't go to infinity within the interval. This makes the concept of area well-defined. We recognize we don't yet know how to calculate areas under curves that don't resemble familiar shapes like rectangles or circles."
    },
    {
        "timestamp": "3:03",
        "summary": "To approximate the area, we divide the interval $[a, b]$ into subintervals, choosing random points $x_1, x_2, \\ldots, x_4$, and raise vertical lines from them to the graph. This process is called a **partition**."
    },
    {
        "timestamp": "4:04",
        "summary": "Within each subinterval, we choose a point $c_i$ and evaluate the function $f(c_i)$, giving the **height** of a rectangle over that subinterval. These rectangles approximate the area under the graph."
    },
    {
        "timestamp": "5:02",
        "summary": "Five rectangles are drawn using the base of each subinterval and height $f(c_i)$. The **sum of their areas** gives an approximation of the total area under the graph—but this estimate includes **visible errors**."
    },
    {
        "timestamp": "6:08",
        "summary": "Some areas are **overcounted** (above the graph), others are **undercounted** (missed below the graph). These approximation errors can be reduced by refining the partition and using **more rectangles**."
    },
    {
        "timestamp": "7:07",
        "summary": "An example is shown: breaking a rectangle into two to improve accuracy. The idea is that finer partitions produce a **closer approximation** to the true area. Errors shrink as the partition improves."
    },
    {
        "timestamp": "8:09",
        "summary": "The process leads to the concept of **Riemann sums**:\n\n\\[ \\sum_{i=1}^n f(c_i) \\Delta x_i \\]\nwhere $\\Delta x_i = x_i - x_{i-1}$ is the subinterval width and $f(c_i)$ is the height of the rectangle."
    },
    {
        "timestamp": "9:13",
        "summary": "We clarify that this sum is an approximation of the area under the graph. By taking more rectangles, we approach a better result, but we still don't reach the exact value—unless we use a **limit**."
    },
    {
        "timestamp": "10:10",
        "summary": "In the limit as $n \\to \\infty$, the Riemann sums converge to the **integral**, denoted temporarily as $I$:\n\n\\[ \\lim_{n \\to \\infty} \\sum_{i=1}^n f(c_i) \\Delta x_i = I \\]\nwhich represents the area under the graph."
    },
    {
        "timestamp": "11:03",
        "summary": "However, simply taking $n \\to \\infty$ isn't precise enough. We must ensure the **entire interval** is refined—not just one part—to capture the correct limiting behavior."
    },
    {
        "timestamp": "12:00",
        "summary": "This introduces the formal idea that a definite integral is the **limit of Riemann sums** over increasingly refined partitions:\n\n\\[ \\int_a^b f(x)\\,dx = \\lim_{\\lambda(P) \\to 0} \\sum_{i=1}^n f(c_i) \\Delta x_i \\]"
    },
    {
        "timestamp": "13:15",
        "summary": "A **partition** of $[a, b]$ is defined as:\n\n\\[ a = x_0 < x_1 < \\ldots < x_n = b \\]\nIt divides the interval into subintervals $[x_{i-1}, x_i]$, over which rectangles are constructed."
    },
    {
        "timestamp": "14:25",
        "summary": "The **width** of each subinterval is:\n\n\\[ \\Delta x_i = x_i - x_{i-1} \\]\nAnd the **mesh** of a partition is:\n\n\\[ \\lambda(P) = \\max \\{ \\Delta x_1, \\Delta x_2, \\ldots, \\Delta x_n \\} \\]"
    },
    {
        "timestamp": "15:35",
        "summary": "We restate the Riemann sum:\n\n\\[ \\sum_{i=1}^n f(c_i) \\Delta x_i \\]\nEach sum depends on the function $f$, the partition $P$, and the choice of points $c_i \\in [x_{i-1}, x_i]$."
    },
    {
        "timestamp": "17:10",
        "summary": "The function $f$ is **Riemann integrable** on $[a, b]$ if the Riemann sums converge to the same value $I$, no matter which $c_i$'s are chosen, as the partition gets finer."
    },
    {
        "timestamp": "18:19",
        "summary": "This is formalized using epsilon-delta language. For every $\\varepsilon > 0$, there exists a $\\delta > 0$ such that if the partition satisfies $\\lambda(P) < \\delta$, then:\n\n\\[ \\left| \\sum_{i=1}^n f(c_i) \\Delta x_i - I \\right| < \\varepsilon \\]"
    },
    {
        "timestamp": "20:20",
        "summary": "This inequality must hold for **any** partition and **any** choice of $c_i$'s. This completes the rigorous definition of **Riemann integrability**."
    },
    {
        "timestamp": "22:03",
        "summary": "The instructor notes this is perhaps the most complex definition of the course. It will be revisited and unpacked next time with more theorems and an introduction to the **Fundamental Theorem of Calculus**."
    }
]

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/app")
def app_page():
    return render_template("index.html", summary_data=SUMMARY_DATA)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def load_csv_to_variable(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

# Path to your CSV file
filepath = r"sample video.csv"

# Load CSV contents into a variable
TRANSCRIPT = load_csv_to_variable(filepath)

def get_text_before_time(time_seconds):
    """
    Return all transcript text segments ending before or at time_seconds (in seconds).
    
    :param time_seconds: float or int, time in seconds
    :return: str, concatenated transcript text before or at time_seconds
    """
    time_ms = int(time_seconds * 1000)  # convert seconds to milliseconds
    parts = []
    for entry in TRANSCRIPT:
        end_time = int(entry['end'])
        if end_time <= time_ms:
            parts.append(entry['text'].strip())
        else:
            break  # assuming TRANSCRIPT is sorted by end time ascending
    
    return " ".join(parts)


@socketio.on('chat_message')
def handle_chat(data):
    """
    Very simple chat stub that distinguishes STT-based vs Internet-based.
    """
    question = data.get('question', '').strip()
    currSec = data.get('currSec', '')
    if not question:
        return
    context = get_text_before_time(currSec)
    general_prompt = f"Given this context, please provide an answer to this question. they are seperated by $$$. context: {context} $$$ question: {question}"
    print(general_prompt)
    # STT-based snippet: find last transcript containing first keyword
    keyword = question.split()[0].lower()
    stt_part = next(
        (e['text'] for e in reversed(transcript_store['sample_lesson'])
         if keyword in e['text'].lower()),
        "(no matching STT snippet)"
    )

    internet_ans = "(example internet-based answer)"
    answer_md = (
        f"**[STT-based]:** {stt_part}\n\n"
        f"**[Internet-based]:** {internet_ans}"
    )

    emit('chat_response', {
        'question': question,
        'answer': answer_md
    }, broadcast=True)

if __name__ == '__main__':
    # Start the background transcription loop
    socketio.run(app, debug=True)
