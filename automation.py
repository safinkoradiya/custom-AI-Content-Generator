import tkinter as tk
from tkinter import ttk, scrolledtext
import requests

API_KEY = "pleasea addd your api key"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

def chat_with_openrouter(prompt):
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("❌ Error:", response.text)
        return None

def generate_script():
    prompt = """
You're a viral content creator for a YouTube Shorts channel called "AI Predicts the Future."

Generate a short-form video script (30 to 60 seconds) that starts with a mind-blowing or shocking hook related to an AI prediction about the future — like jobs, relationships, money, education, health, creativity, or technology.

Use conversational, American-style English that feels like it's made for TikTok or YouTube Shorts. Make it punchy, curious, and simple. Avoid technical words.

Then explain the AI prediction briefly — what it says, why it matters.

End with an open-ended question or curiosity line to drive engagement. Every script must be under 100 words.

Output format:
- Title
- Script (for voiceover/video)
"""
    return chat_with_openrouter(prompt)

def generate_dark_script():
    prompt = """
You're a viral content creator for a YouTube Shorts channel called "The Dark Side of Everyday Things."

Generate a short, 30–60 second video script that exposes a surprising, shocking, or unsettling truth about something common — like social media, smartphones, energy drinks, fast food, clothing brands, school systems, mobile apps, daily habits, etc.

Start the script with a strong, attention-grabbing hook. Then explain the hidden dark side in a way that's clear, simple, and emotionally engaging. Use casual, conversational American English (like how people talk on TikTok or YouTube Shorts). Keep the tone a bit dramatic or mysterious.

End with a punchy curiosity or question to keep the viewer thinking or wanting more. Keep the script under 100 words.

Output format:
- Title
- Script
"""
    return chat_with_openrouter(prompt)

def format_for_voiceover(script):
    if not script:
        return None
    prompt = f"""
You're a voice director and script localizer for a US-based YouTube Shorts channel.

Take the following script and rewrite it in natural, conversational American English that sounds familiar and relatable to US viewers. Use casual but clear vocabulary — avoid formal or robotic tone. Feel free to use everyday American phrases and sentence structures.

Then, format it with inline emotional direction tags (for AI text-to-speech) such as:
- [excited]
- [pause]
- [serious]
- [curious tone]
- [emotional]
- [dramatic pause]
- [whisper]

Make sure the final version feels like something a real American creator would say — like a TikTok or YouTube Shorts voiceover. Keep it short and punchy for a 30–60 second video.

Script:

{script}
"""
    return chat_with_openrouter(prompt)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔮 AI Content Generator")
        self.geometry("900x720")
        self.configure(bg="#2B2B2B")

        style = ttk.Style(self)
        style.theme_use('default')
        style.configure("TButton", font=("Segoe UI", 12), padding=10, relief="flat",
                        background="#3C3C3C", foreground="#FFFFFF")
        style.map("TButton", background=[('active', '#5C5C5C')])

        container = tk.Frame(self, bg="#2B2B2B")
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, ScriptGenPage, VoiceoverPage, DarkSidePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2B2B2B")
        tk.Label(self, text="🧠 AI Automation Tools", font=("Segoe UI", 22),
                 bg="#2B2B2B", fg="white").pack(pady=40)

        ttk.Button(self, text="🎬 Generate AI Prediction Script",
                   command=lambda: controller.show_frame("ScriptGenPage")).pack(pady=10)

        ttk.Button(self, text="🎙️ Rewrite with Voiceover Emotions",
                   command=lambda: controller.show_frame("VoiceoverPage")).pack(pady=10)

        ttk.Button(self, text="☠️ Generate 'Dark Side' Script",
                   command=lambda: controller.show_frame("DarkSidePage")).pack(pady=10)

class ScriptGenPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2B2B2B")
        tk.Label(self, text="🎬 Generate AI Prediction Script", font=("Segoe UI", 18),
                 bg="#2B2B2B", fg="white").pack(pady=10)

        self.status = tk.Label(self, text="", font=("Segoe UI", 10),
                               bg="#2B2B2B", fg="#88FF88")
        self.status.pack()

        tk.Label(self, text="📝 Generated Script:", font=("Segoe UI", 12),
                 bg="#2B2B2B", fg="white").pack()

        self.text_output = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                                     width=100, height=25,
                                                     font=("Courier", 10),
                                                     bg="#1F1F28", fg="white")
        self.text_output.pack(padx=10, pady=5)
        self.text_output.configure(state='disabled')

        ttk.Button(self, text="Generate Script", command=self.run).pack(pady=5)
        ttk.Button(self, text="← Home", command=lambda: controller.show_frame("HomePage")).pack(pady=(10, 0))

    def run(self):
        self.status.config(text="⏳ Generating…")
        self.after(100, self._generate_script)

    def _generate_script(self):
        script = generate_script()
        self.text_output.configure(state='normal')
        self.text_output.delete(1.0, tk.END)

        if script:
            self.text_output.insert(tk.END, script)
            with open("ai_script.txt", "w", encoding="utf-8") as f:
                f.write(script)
            self.status.config(text="✅ Script saved successfully!")
        else:
            self.text_output.insert(tk.END, "❌ Failed to generate script.")
            self.status.config(text="❌ Error generating script.")
        self.text_output.configure(state='disabled')

class VoiceoverPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2B2B2B")
        tk.Label(self, text="🎙️ Voiceover Rewrite with Emotion Tags", font=("Segoe UI", 18),
                 bg="#2B2B2B", fg="white").pack(pady=10)

        self.status = tk.Label(self, text="", font=("Segoe UI", 10),
                               bg="#2B2B2B", fg="#88FF88")
        self.status.pack()

        self.input_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100,
                                                    height=10, font=("Courier", 10),
                                                    bg="#1F1F28", fg="white")
        self.input_text.pack(padx=10, pady=5)
        self.input_text.insert(tk.END, "Paste your script here...")

        ttk.Button(self, text="Rewrite with Emotions", command=self.rewrite).pack(pady=5)

        tk.Label(self, text="📝 Output:", font=("Segoe UI", 12),
                 bg="#2B2B2B", fg="white").pack()

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100,
                                                     height=15, font=("Courier", 10),
                                                     bg="#1F1F28", fg="white")
        self.output_text.pack(padx=10, pady=5)
        self.output_text.configure(state='disabled')

        ttk.Button(self, text="← Home", command=lambda: controller.show_frame("HomePage")).pack(pady=(10, 0))

    def rewrite(self):
        self.status.config(text="⏳ Rewriting...")
        script = self.input_text.get("1.0", tk.END).strip()
        self.after(100, lambda: self._rewrite_script(script))

    def _rewrite_script(self, script):
        result = format_for_voiceover(script)
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)

        if result:
            self.output_text.insert(tk.END, result)
            with open("ai_voiceover_script.txt", "w", encoding="utf-8") as f:
                f.write(result)
            self.status.config(text="✅ Script saved successfully!")
        else:
            self.output_text.insert(tk.END, "❌ Failed to rewrite.")
            self.status.config(text="❌ Error rewriting.")
        self.output_text.configure(state='disabled')

class DarkSidePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2B2B2B")
        tk.Label(self, text="☠️ Generate Dark Side Script", font=("Segoe UI", 18),
                 bg="#2B2B2B", fg="white").pack(pady=10)

        self.status = tk.Label(self, text="", font=("Segoe UI", 10),
                               bg="#2B2B2B", fg="#88FF88")
        self.status.pack()

        tk.Label(self, text="📝 Generated Script:", font=("Segoe UI", 12),
                 bg="#2B2B2B", fg="white").pack()

        self.text_output = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                                     width=100, height=25,
                                                     font=("Courier", 10),
                                                     bg="#1F1F28", fg="white")
        self.text_output.pack(padx=10, pady=5)
        self.text_output.configure(state='disabled')

        ttk.Button(self, text="Generate Dark Side Script", command=self.run).pack(pady=5)
        ttk.Button(self, text="← Home", command=lambda: controller.show_frame("HomePage")).pack(pady=(10, 0))

    def run(self):
        self.status.config(text="⏳ Generating…")
        self.after(100, self._generate_dark_script)

    def _generate_dark_script(self):
        script = generate_dark_script()
        self.text_output.configure(state='normal')
        self.text_output.delete(1.0, tk.END)

        if script:
            self.text_output.insert(tk.END, script)
            with open("dark_side_script.txt", "w", encoding="utf-8") as f:
                f.write(script)
            self.status.config(text="✅ Script saved successfully!")
        else:
            self.text_output.insert(tk.END, "❌ Failed to generate script.")
            self.status.config(text="❌ Error generating script.")
        self.text_output.configure(state='disabled')

if __name__ == "__main__":
    app = App()
    app.mainloop()
