# summarizer.py
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

class VideoSummarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def extract_video_id(self, url):
        match = re.search(r"(?:v=|youtu\.be/)([^\&\n]+)", url)
        return match.group(1) if match else None

    def fetch_transcript(self, video_id):
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text

    def summarize_transcript(self, text):
        if len(text) > 1024:
            text = text[:1024]  # truncate if too long
        summary = self.summarizer(text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def summarize_video(self, video_url):
        video_id = self.extract_video_id(video_url)
        transcript = self.fetch_transcript(video_id)
        return self.summarize_transcript(transcript)
