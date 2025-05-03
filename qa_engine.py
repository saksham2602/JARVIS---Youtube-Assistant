from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import re

class QAEngine:
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    def get_transcript(self, youtube_url):
        video_id = self.extract_video_id(youtube_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return full_text

    def extract_video_id(self, url):
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        return match.group(1) if match else None

    def answer_question(self, url, question):
        print("📼 Getting transcript...")
        context = self.get_transcript(url)
        print("🤖 Answering your question...")
        answer = self.qa_pipeline(question=question, context=context[:3000])  # keep it short enough
        return answer["answer"]
