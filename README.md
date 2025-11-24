# Monitor Agent Prototype – Assignment

This project monitors a **live TV stream**, creates **transcripts**, and makes a **short summary every 1 minute**.

## What It Does

- Captures LiveNOW Fox stream (m3u8)
- Cuts audio into 60-second files
- Converts audio → text using Whisper
- Generates short summary using BART
- Sends updates live to webpage using WebSocket
- Shows timestamp, transcript, summary

## Requirements Completed

✔ Live feed capture  
✔ 60s audio segments  
✔ Whisper transcription  
✔ BART summarization  
✔ Real-time UI updates  
✔ Start/Stop buttons  
✔ Simple frontend  

## Why I Used These Tools

I tried OpenAI and Gemini first but free credits got over.  
So I used **local AI models** (Whisper + BART) which are free and run offline.

## Tech Stack

- Django + DRF  
- Django Channels (WebSockets)  
- FFmpeg  
- Whisper + BART  
- HTML / CSS / JavaScript  
- SQLite  

## Project Structure

```
monitor_agent/
│── monitor/ (processing code)
│── templates/index.html
│── static/
│── media/segments/
```

## How to Run

1. Install Python 3.11+ and FFmpeg  
2. Create venv  
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install requirements  
   ```
   pip install -r requirements.txt
   ```
4. Run migrations  
   ```
   python manage.py migrate
   ```
5. Start server  
   ```
   python manage.py runserver
   ```
6. Open browser: http://localhost:8000  
7. Click **Start Monitoring**  
8. First output comes after ~60 sec  

## How It Works (Simple)

1. User clicks Start  
2. FFmpeg records the live stream  
3. Creates 60-second audio segment  
4. Whisper → transcribes  
5. BART → summarizes  
6. WebSocket → sends to frontend  
7. UI updates the table  
8. Repeat for next segment  
9. User clicks Stop → FFmpeg stops  

## Data Flow (Step-by-Step)

- User opens browser  
- Loads `index.html`  
- WebSocket connects  
- User clicks **Start**  
- `POST /api/start/`  
- FFmpeg starts recording  
- Creates 60s segment  
- Monitor thread detects new file  
- Whisper transcribes  
- BART summarizes  
- WebSocket sends update  
- Frontend shows result  
- User clicks **Stop**  
- `POST /api/stop/`  
- FFmpeg + thread stop  

## FFmpeg Blocking Note

FFmpeg prints a lot of messages.  
If we don’t redirect them to a log file, **Python hangs** because the output buffer gets full.

## Issues I Faced

- API credits finished → moved to local models  
- FFmpeg blocking → fixed with log file  
- Stream URL finding  
- WebSocket setup  
- Large model downloads  

## Submission

**Name:** Vanshul  
**Assignment:** Monitor Agent Prototype  
**Deadline:** Tuesday, 9:30 AM  
