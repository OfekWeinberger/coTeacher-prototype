```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CoTeacher (SocketIO)</title>
  <!-- Socket.IO -->
  <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
  <!-- Marked.js for Markdown rendering -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <!-- MathJax for LaTeX rendering -->
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <!-- TailwindCSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Poppins font -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: radial-gradient(circle at center, #fff3e0, #f9f7f4);
      color: #2c2c2c;
      height: 100vh;
      overflow: hidden;
      display: flex;
    }
    .panel {
      background: rgba(255, 255, 255, 0.9);
      border-radius: 1rem;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    #summary-panel, #chat-panel {
      width: 25%;
      height: 100%;
    }
    #video-panel {
      flex: 1;
      height: 100%;
    }
    .markdown-body h1, .markdown-body h2, .markdown-body h3 {
      font-weight: 600;
      margin-top: 1em;
      margin-bottom: 0.5em;
    }
    .markdown-body p {
      margin-bottom: 1em;
      line-height: 1.5;
    }
    .markdown-body ul, .markdown-body ol {
      padding-left: 1.5em;
      margin-bottom: 1em;
    }
    .markdown-body code {
      background: #f1f1f1;
      padding: 2px 4px;
      border-radius: 4px;
      font-family: monospace;
    }
    .markdown-body pre {
      background: #f1f1f1;
      padding: 1em;
      border-radius: 6px;
      overflow: auto;
      margin-bottom: 1em;
    }
    .markdown-body blockquote {
      border-left: 4px solid #ddd;
      padding-left: 1em;
      color: #666;
      margin-bottom: 1em;
    }
    /* Scrollbars */
    .panel::-webkit-scrollbar { width: 8px; }
    .panel::-webkit-scrollbar-thumb { background: #ccc; border-radius: 4px; }
    .panel::-webkit-scrollbar-thumb:hover { background: #bbb; }
  </style>
</head>
<body>
  <div class="flex w-full h-full">
    <!-- Summary panel -->
    <div id="summary-panel" class="panel p-4">
      <h4 class="text-xl font-semibold mb-4">📝 Live Summary</h4>
      <div id="summary-text" class="markdown-body flex-1 overflow-auto p-2">
        <p>Loading summary...</p>
      </div>
    </div>

    <!-- Video panel -->
    <div id="video-panel" class="panel p-4 flex items-center justify-center">
      <video id="video" controls class="rounded-2xl shadow-lg w-full h-auto max-h-[90vh]">
        <source src="/static/sample_lesson.mp4" type="video/mp4">
        Your browser does not support HTML video.
      </video>
    </div>

    <!-- Chat panel -->
    <div id="chat-panel" class="panel p-4">
      <h4 class="text-xl font-semibold mb-4">💬 Ask Questions</h4>
      <div id="chat-log" class="flex-1 overflow-auto p-2 markdown-body"></div>
      <div class="mt-4 flex gap-2">
        <input type="text" id="user-input" placeholder="Ask a question..."
          class="flex-1 bg-white/80 text-gray-800 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-300 transition" />
        <button onclick="askQuestion()"
          class="bg-orange-400 text-white font-semibold px-6 py-2 rounded-lg hover:bg-orange-500 transition">Send</button>
      </div>
    </div>
  </div>

  <script>
    const socket = io();

    // Render Markdown and LaTeX for summary
    socket.on("summary_update", data => {
      const el = document.getElementById("summary-text");
      el.innerHTML = marked.parse(data.summary);
      MathJax.typesetPromise([el]);
    });

    // Chat responses
    socket.on("chat_response", data => {
      const log = document.getElementById("chat-log");
      const msg = document.createElement("div");
      msg.className = "mb-4";
      msg.innerHTML = marked.parse(`**You:** ${data.question}\n\n**CoTeacher:** ${data.answer}`);
      log.appendChild(msg);
      MathJax.typesetPromise([msg]);
      log.scrollTop = log.scrollHeight;
    });

    function askQuestion() {
      const input = document.getElementById("user-input");
      const question = input.value.trim();
      if (!question) return;
      socket.emit("chat_message", { question });
      input.value = "";
    }
  </script>
</body>
</html>
