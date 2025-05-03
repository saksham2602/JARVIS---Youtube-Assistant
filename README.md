
# JARVIS – YouTube Voice Assistant 🎙️📺

An AI-powered voice and gesture-controlled assistant that interacts with YouTube videos — enabling hands-free control through natural voice commands and hand gestures using deep learning and computer vision.

## 🔧 Features

- 🎤 **Voice Command Recognition** using SpeechRecognition and a Keras-trained NLP model.
- ✋ **Gesture Control** with OpenCV and MediaPipe for intuitive, silent interactions.
- 📺 Supports 10+ YouTube video actions: play, pause, next, volume up/down, mute, fullscreen, etc.
- 🤖 Custom intent detection model with **92% accuracy**.
- 🔄 Real-time interaction with audio-gesture sync.
- 💡 Modular architecture for expansion to other platforms (e.g. Spotify, VLC).

## 🧠 Tech Stack

- **Python**
- **TensorFlow / Keras** – for intent recognition
- **SpeechRecognition** – for real-time voice input
- **OpenCV + MediaPipe** – for hand gesture recognition
- **PyAutoGUI** – for GUI-based control of YouTube playback


- **Two different models** - {a.pkl,b.pkl} Classifier Models
                        {intent_classifier_model.pkl,vectorizer.pkl} Tensorflow Model

*Built with ❤️ by Saksham Bhatia*
