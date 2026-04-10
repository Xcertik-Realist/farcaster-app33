from flask import Flask, render_template, request, redirect
import datetime
import os

# Explicitly set template folder path for Vercel compatibility
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=template_dir)

# In-memory notes (reset on cold starts - normal for Vercel)
notes = []

@app.route("/")
def home():
    try:
        return render_template("index.html", notes=notes)
    except Exception as e:
        return f"""
        <h2>Template Error</h2>
        <p>{str(e)}</p>
        <p>Current working dir: {os.getcwd()}</p>
        <p>Template folder set to: {app.template_folder}</p>
        """, 500

@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title", "Untitled").strip()
    content = request.form.get("content", "").strip()
    
    if content:
        notes.append({
            "id": len(notes) + 1,
            "title": title or "Untitled",
            "content": content,
            "time": datetime.datetime.now().strftime("%b %d, %H:%M")
        })
    
    return redirect("/")

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return redirect("/")

# Required for Vercel
app = app
