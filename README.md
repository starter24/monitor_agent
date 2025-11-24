# Monitor Agent Prototype - Assignment Submission

## Assignment Objective

Build a system that monitors a live TV feed from https://www.livenowfox.com/live and generates transcripts + AI summaries every minute.

## What I Built

This app watches the live TV stream, extracts audio every 60 seconds, converts speech to text, and creates short summaries. Everything updates in real-time on a webpage.

## Assignment Requirements Met

✅ **Live Feed**: Using FFmpeg to capture stream from LiveNOW Fox (m3u8 URL)  
✅ **Audio Extraction**: Continuous extraction, saved as 60-second segments  
✅ **Transcription**: Speech-to-text every 1 minute using Whisper  
✅ **AI Summary**: Short summaries (15-20 words) using BART  
✅ **Output**: Displays Timestamp, Transcript, and Summary  
✅ **UI**: Simple frontend with Start/Stop buttons  
✅ **Real-time**: WebSocket updates, appears ~70-80 seconds after being spoken on TV

## Why I Used These Technologies

### AI Models
I tried using OpenAI Whisper API and Google Gemini API first, but both ran out of free credits. So I switched to:
- **Whisper (local)** - runs on my computer, completely free
- **BART (Facebook)** - also runs locally, no API needed

This way the whole system is free to run and doesn't need internet after initial setup.

### Backend
- **Django** - because it's easy to set up and has good documentation
- **Django Channels** - for WebSocket support (real-time updates)
- **FFmpeg** - industry standard for handling video/audio streams

## Tech Stack

- Backend: Django + Django REST Framework
- Real-time: Django Channels (WebSockets)
- Stream Processing: FFmpeg
- AI Models: Whisper (transcription) + BART (summarization)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (default Django)

## Project Structure

```
monitor_agent/
├── manage.py
├── requirements.txt
├── monitor_agent/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py            # WebSocket config
├── monitor/                # Main app
│   ├── views.py           # API endpoints (start/stop/status)
│   ├── consumers.py       # WebSocket handler
│   ├── stream_handler.py  # FFmpeg + processing logic
│   ├── transcriber.py     # Whisper integration
│   └── summarizer.py      # BART integration
├── templates/
│   └── index.html         # Frontend UI
├── static/
│   ├── css/style.css
│   └── js/script.js
└── media/segments/        # Audio files saved here
```

## How to Run

### Prerequisites
1. Python 3.11+
2. FFmpeg (install using `winget install -e --id Gyan.FFmpeg`)

### Installation Steps

1. **Clone/Download the project**

2. **Create virtual environment**:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
   Note: First time will download AI models (~2GB), takes 5-10 minutes

4. **Navigate to project folder**:
   ```
   cd monitor_agent
   ```

5. **Run migrations**:
   ```
   python manage.py migrate
   ```

6. **Start the server**:
   ```
   python manage.py runserver
   ```

7. **Open browser**: Go to `http://localhost:8000`

8. **Click "Start Monitoring"** and wait ~60 seconds for first result

9. **Stop**: Press `Ctrl+C` in terminal or click "Stop Monitoring" button

## How It Works (Simple Explanation)

1. **User clicks "Start Monitoring"**
   - Browser sends request to Django server
   - Server starts FFmpeg process

2. **FFmpeg captures live stream**
   - Downloads audio from LiveNOW Fox stream
   - Saves 60-second chunks as MP3 files

3. **Python monitors for new files**
   - Background thread checks for new audio files every 5 seconds

4. **When new file found**:
   - Whisper converts audio → text
   - BART summarizes text → short summary
   - WebSocket sends data to browser

5. **Browser displays result**
   - New row added to table with timestamp, transcript, summary

## Performance

- **Latency**: ~70-80 seconds from "spoken on TV" to "appears on screen"
  - 60 seconds: segment duration
  - 5-10 seconds: Whisper transcription
  - 2-3 seconds: BART summarization
  - 5 seconds: monitoring loop delay

- **Resource Usage**:
  - RAM: ~4GB (for AI models)
  - CPU: Moderate (depends on PC)

## Challenges I Faced

1. **API Quota Issues**: OpenAI and Gemini ran out of credits, had to switch to local models
2. **FFmpeg Deadlock**: Output buffer was filling up, fixed by redirecting to log file
3. **Stream URL**: Original URL was dead, found working alternative
4. **WebSocket Setup**: Had to configure Django Channels properly
5. **Model Download**: BART model is 1.6GB, takes time on first run

## Screenshots

<img width="1894" height="827" alt="Screenshot 2025-11-24 212814" src="https://github.com/user-attachments/assets/48e84e45-0d0e-4a0a-a343-374109263338" />


## Testing

Tested with:
- Live stream running for 10+ minutes
- Multiple start/stop cycles
- Verified real-time updates via WebSocket
- Checked transcript accuracy against actual TV audio

## Notes

- First run downloads AI models, be patient
- Audio segments saved in `media/segments/` folder
- Check `ffmpeg.log` if stream issues
- Works offline after initial setup

## Submission Details

- **Student**: Vanshul
- **Deadline**: Tuesday, 9:30 AM
- **Assignment**: Monitor Agent Prototype

---

### Troubleshooting

**Nothing showing up?**
- Wait at least 60 seconds after clicking Start
- Check terminal for errors
- Look at ffmpeg.log file

**Server won't start?**
- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

**Out of memory?**
- Close other apps
- AI models need ~4GB RAM

---

Built using free/open-source tools only. No API costs.
