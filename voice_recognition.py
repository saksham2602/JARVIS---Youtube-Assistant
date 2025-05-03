from intent_classifier import IntentPredictor
from query_extractor import QueryExtractor
from recommendations import Recommendation
from summarizer import VideoSummarizer
from gesture_recognition import GestureRecognition
from qa_engine import QAEngine
import speech_recognition as sr
import pyautogui
import pyperclip
import threading
import re

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.predictor = IntentPredictor()  # Your pre-trained classifier
        self.video_summarizer = VideoSummarizer()
        self.recommendation = Recommendation()
        self.query_extractor = QueryExtractor()
        self.gesture_controller = GestureRecognition()
        self.qa_engine = QAEngine()
        
        self.gesture_thread = None
        self.gesture_active = False
        self._setup_intent_actions()

    def _setup_intent_actions(self):
        """Maps all intents to their corresponding actions"""
        self.intent_actions = {
            'play': self._handle_play,
            'pause': self._handle_pause,
            'volume_up': self._handle_volume_up,
            'volume_down': self._handle_volume_down,
            'fast_forward': self._handle_fast_forward,
            'rewind': self._handle_rewind,
            'next_video': self._handle_next,
            'previous_video': self._handle_previous,
            'gesture_on': self._handle_gesture_on,
            'gesture_off': self._handle_gesture_off,
            'search': self._handle_search,
            'summarize': self._handle_summarize,
            'question': self._handle_question,
            'mute': self._handle_mute,
            'unmute': self._handle_unmute,
            'seek_to': self._handle_seek_to,
            'play_first_video': self._handle_play_first_video  # ✅ NEW
    }

    def listen_for_commands(self):
        with sr.Microphone() as source:
            print("🎙️ Listening for commands...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(f"🗣️ Command received: {command}")
                return command
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
                return ""

    def process_command(self, command):
        intent = self.predictor.predict(command)
        print(f"🔮 Detected intent: {intent}")
        
        if intent in self.intent_actions:
            self.intent_actions[intent](command)
        else:
            print(f"⚠️ No handler for intent: {intent}")

    # --- Intent Handlers ---
    def _handle_play(self, command):
        pyautogui.press('k')
        print("▶️ Playing video...")

    def _handle_pause(self, command):
        pyautogui.press('k')
        print("⏸️ Pausing video...")

    def _handle_volume_up(self, command):
        times = 3 if "a little" in command or "bit" in command else 8
        for _ in range(times):
            pyautogui.press('up')
        print(f"🔊 Increased volume ({times} steps)")

    def _handle_volume_down(self, command):
        times = 3 if "a little" in command or "bit" in command else 8
        for _ in range(times):
            pyautogui.press('down')
        print(f"🔉 Decreased volume ({times} steps)")

    def _handle_fast_forward(self, command):
        pyautogui.press('l')
        print("⏩ Fast forwarded 10 seconds")

    def _handle_rewind(self, command):
        pyautogui.press('j')
        print("⏪ Rewound 10 seconds")

    def _handle_next(self, command):
        pyautogui.hotkey('shift', 'n')
        print("⏭️ Next video")

    def _handle_previous(self, command):
        pyautogui.hotkey('shift', 'p')
        print("⏮️ Previous video")

    def _handle_gesture_on(self, command):
        if not self.gesture_active:
            print("🟢 Starting gesture control...")
            self.gesture_thread = threading.Thread(target=self.gesture_controller.start)
            self.gesture_thread.start()
            self.gesture_active = True

    def _handle_gesture_off(self, command):
        if self.gesture_active:
            print("🔴 Stopping gesture control...")
            self.gesture_controller.stop()
            self.gesture_active = False

    def _handle_search(self, command):
        # Check if user said: "play first video"
        if "play first video" in command:
            print("▶️ Playing the first video from search results...")
            pyautogui.sleep(2)  # Wait for results to load
            pyautogui.press('tab', presses=20, interval=0.2)  # Navigate to first video
            pyautogui.press('enter')
        else:
            # Default search behavior
            query = self.query_extractor.extract_search_query(command)
            print(f"🔍 Searching for: {query}")
            pyautogui.press('/')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            pyautogui.write(query)
            pyautogui.press('enter')
    def _handle_play_first_video(self, command):
            print("▶️ Playing the first video from search results...")
            pyautogui.sleep(2)  # Give YouTube time to load results
            pyautogui.moveTo(1253,374)
            pyautogui.click()



    def _handle_summarize(self, command):
        print("📋 Fetching summary...")
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        url = pyperclip.paste()
        if "youtube.com" in url:
            try:
                summary = self.video_summarizer.summarize_video(url)
                print(f"\n📚 Summary:\n{summary}")
            except Exception as e:
                print(f"⚠️ Summarization failed: {e}")

    def _handle_question(self, command):
        question = command.replace("question", "").strip()
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        url = pyperclip.paste()
        if "youtube.com" in url:
            try:
                answer = self.qa_engine.answer_question(url, question)
                print(f"💡 Answer: {answer}")
            except Exception as e:
                print(f"⚠️ QA failed: {e}")

    def _handle_mute(self, command):
        pyautogui.press('m')
        print("🔇 Muted")

    def _handle_unmute(self, command):
        pyautogui.press('m')
        print("🔊 Unmuted")

    def _handle_seek_to(self, command):
        try:
            minutes = int(re.search(r'\d+', command).group())
            print(f"⏱️ Seeking to {minutes} minute(s)...")
            pyautogui.press('/')
            pyautogui.write(f"{minutes}:00")
            pyautogui.press('enter')
        except:
            print("⚠️ Couldn't parse timestamp")