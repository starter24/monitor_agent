import os
import subprocess
import threading
import time
import glob
from django.conf import settings
from .transcriber import transcribe_audio
from .summarizer import summarize_text
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class StreamMonitor:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.process = None
        self.running = False
        self.output_dir = os.path.join(settings.BASE_DIR, 'media', 'segments')
        os.makedirs(self.output_dir, exist_ok=True)
        self.monitor_thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        
        # Clean up old segments
        for f in glob.glob(os.path.join(self.output_dir, "*")):
            try:
                os.remove(f)
            except Exception as e:
                print(f"Error removing file {f}: {e}")

        # Start FFmpeg
        # ffmpeg -i URL -f segment -segment_time 60 -c:a libmp3lame -b:a 128k -vn segment_%03d.mp3
        ffmpeg_path = r'C:\Users\Vanshul\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe'
        command = [
            ffmpeg_path,
            '-i', self.stream_url,
            '-f', 'segment',
            '-segment_time', '60',
            '-reset_timestamps', '1',
            '-c:a', 'libmp3lame',
            '-b:a', '128k',
            '-vn',
            os.path.join(self.output_dir, 'segment_%03d.mp3')
        ]
        
        # Use shell=False for security, but ensure ffmpeg is in PATH
        self.log_file = open(os.path.join(settings.BASE_DIR, 'ffmpeg.log'), 'w')
        self.process = subprocess.Popen(command, stdout=self.log_file, stderr=self.log_file)
        
        self.monitor_thread = threading.Thread(target=self.monitor_segments)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.close()

    def monitor_segments(self):
        print("Monitoring segments started...")
        processed_files = set()
        while self.running:
            if self.process and self.process.poll() is not None:
                print("FFmpeg process exited unexpectedly! Check ffmpeg.log for details.")
                self.running = False
                break

            files = sorted(glob.glob(os.path.join(self.output_dir, "*.mp3")))
            print(f"Found {len(files)} segments: {files}")
            # Process all but the last one (which is currently being written)
            if len(files) > 1:
                for f in files[:-1]:
                    if f not in processed_files:
                        print(f"Processing new segment: {f}")
                        self.process_segment(f)
                        processed_files.add(f)
            time.sleep(5)

    def process_segment(self, file_path):
        print(f"Processing {file_path}")
        # Transcribe
        transcript = transcribe_audio(file_path)
        print(f"Transcript: {transcript[:50]}...")
        # Summarize
        summary = summarize_text(transcript)
        print(f"Summary: {summary}")
        
        # Broadcast
        channel_layer = get_channel_layer()
        print(f"Broadcasting to group monitor_updates")
        async_to_sync(channel_layer.group_send)(
            "monitor_updates",
            {
                "type": "monitor_update",
                "data": {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "transcript": transcript,
                    "summary": summary,
                    "file": os.path.basename(file_path)
                }
            }
        )

# Global instance
monitor_instance = StreamMonitor("https://fox-foxnewsnow-vizio.amagi.tv/playlist.m3u8")
