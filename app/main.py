from pathlib import Path
from datetime import datetime
import sqlite3
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'data' / 'brother.db'
DB.parent.mkdir(exist_ok=True)
app = FastAPI(title='BROTHER AI')


def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with connect() as con:
        con.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        con.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL)')
        con.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('name','BROTHER')")

init_db()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)

class SettingsRequest(BaseModel):
    name: str = Field(min_length=1, max_length=40)


def get_name():
    with connect() as con:
        return con.execute("SELECT value FROM settings WHERE key='name'").fetchone()['value']


def reply(message: str):
    lower = message.casefold().strip()
    name = get_name()
    if lower in ('hi', 'hello', 'salam', 'assalamualaikum'):
        return f'Assalam-o-Alaikum bhai! Main {name} hoon.'
    if 'time' in lower or 'waqt' in lower:
        return datetime.now().strftime('Abhi %I:%M %p hai.')
    if 'date' in lower or 'tareekh' in lower:
        return datetime.now().strftime('Aaj %d %B %Y hai.')
    return 'Bhai, aapka message save ho gaya. Abhi mera AI brain connect nahi hua; aglay version mein natural replies aayenge.'

@app.get('/')
def home():
    return FileResponse(ROOT / 'frontend' / 'index.html')

@app.get('/api/history')
def history():
    with connect() as con:
        return [dict(row) for row in con.execute('SELECT id, role, content, created_at FROM messages ORDER BY id ASC LIMIT 500')]

@app.get('/api/settings')
def settings():
    return {'name': get_name()}

@app.put('/api/settings')
def update_settings(payload: SettingsRequest):
    with connect() as con:
        con.execute("UPDATE settings SET value=? WHERE key='name'", (payload.name.strip(),))
    return {'name': get_name()}

@app.post('/api/chat')
def chat(payload: ChatRequest):
    answer = reply(payload.message)
    now = datetime.now().isoformat(timespec='seconds')
    with connect() as con:
        con.execute('INSERT INTO messages(role, content, created_at) VALUES(?,?,?)', ('user', payload.message, now))
        con.execute('INSERT INTO messages(role, content, created_at) VALUES(?,?,?)', ('assistant', answer, now))
    return {'reply': answer}
