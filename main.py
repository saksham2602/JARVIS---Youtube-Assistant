from voice_recognition import VoiceRecognition
from recommendations import Recommendation
import time
import pyautogui
import time
import tensorflow as tf
import logging

# Set TensorFlow log level to ERROR to suppress warnings
tf.get_logger().setLevel(logging.ERROR)




def main():
    voice_recognition = VoiceRecognition()
    recommendation_system = Recommendation()

    print("🧠 AI Assistant is running. Say a command like 'play', 'pause', or 'use gesture control'.")

    while True:
        # 1. Voice listens continuously
        command = voice_recognition.listen_for_commands()
        if command:
            voice_recognition.process_command(command)

        # 2. (Optional) You can fetch recommendations once or on some keyword
        if "recommend" in command:
            recommendations = recommendation_system.get_recommendations()
            print("\n🎯 Recommended Videos:\n")
            for idx, title in enumerate(recommendations, start=1):
                print(f"{idx}. {title}")
            print("\nSay another command:")

        # 3. Optional: Add a delay to reduce CPU usage
        time.sleep(0.5)

if __name__ == "__main__":
    main()
