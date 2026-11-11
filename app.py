from flask import Flask, render_template_string, request
import socket
import requests

app = Flask(__name__)

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberSec Toolkit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0b0f19; color: #e2e8f0; }
        .glass-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(51, 65, 85, 0.5); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-between p-4">

    <header class="w-full max-w-2xl text-center py-6">
        <h1 class="text-3xl font-bold text-cyan-400 tracking-wider">CYBER_TOOLKIT</h1>
        <p class="text-sm text-slate-400 mt-1">Lightweight Python Security Scanner Hub</p>
    </header>

    <main class="w-full max-w-2xl glass-card rounded-2xl p-6 shadow-2xl">
        <form method="POST" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Select Tool:</label>
                <select name="tool_type" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-cyan-400">
                    <option value="dns">DNS Lookup (IP Resolver)</option>
                    <option value="headers">Security Headers Checker</option>
                </select>
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Target (Domain or URL):</label>
                <input type="text" name="target" placeholder="e.g., example.com" required
                    class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-cyan-400">
            </div>

            <button type="submit" 
                class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-3 rounded-lg transition duration-200 shadow-lg shadow-cyan-500/20">
                Run Analysis
            </button>
        </form>

        {% if result %}
        <div class="mt-6 p-4 bg-slate-950/80 border border-cyan-500/30 rounded-xl">
            <h3 class="text-sm font-semibold text-cyan-400 mb-2 uppercase tracking-wide">Output Result:</h3>
            <pre class="whitespace-pre-wrap text-sm font-mono text-emerald-400 overflow-x-auto">{{ result }}</pre>
        </div>
        {% endif %}
    </main>

    <footer class="text-xs text-slate-500 py-4">
        Built with Python & Flask • For Educational Purposes Only
    </footer>

</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        tool_type = request.form.get('tool_type')
        target = request.form.get('target').strip()
        
        try:
            if tool_type == 'dns':
                clean_target = target.replace("https://", "").replace("http://", "").split("/")[0]
                ip = socket.gethostbyname(clean_target)
                result = f"[+] Target: {clean_target}\n[+] Resolved IP: {ip}"
                
            elif tool_type == 'headers':
                if not target.startswith('http'):
                    target = 'https://' + target
                response = requests.get(target, timeout=5)
                headers = response.headers
                sec_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']
                
                output = f"Security Headers Check for: {target}\n" + "-"*40 + "\n"
                for h in sec_headers:
                    if h in headers:
                        output += f"[PRESENT] {h}\n"
                    else:
                        output += f"[MISSING] {h}\n"
                result = output
        except Exception as e:
            result = f"[-] Error executing tool: {str(e)}"
            
    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
