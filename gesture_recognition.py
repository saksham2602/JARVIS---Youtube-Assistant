import cv2
import mediapipe as mp
import pyautogui
import threading
import time

class GestureRecognition:
    def __init__(self):
        self.running = False
        self.thread = None
        self.lock = threading.Lock()  # Ensure thread safety
        self.last_gesture = None

    def get_finger_states(self, landmarks):
        # Define tip and PIP ids for each finger
        tip_ids = [4, 8, 12, 16, 20]
        pip_ids = [3, 7, 11, 15, 19]
        
        fingers = []
        
        for i in range(5):
            if landmarks.landmark[tip_ids[i]].y < landmarks.landmark[pip_ids[i]].y:
                fingers.append(1)  # Finger is up
            else:
                fingers.append(0)  # Finger is down
        
        return fingers

    def classify_gesture(self, fingers):
        # Define gestures based on finger state patterns
        if fingers == [1, 1, 1, 1, 1]: 
            return "Play"
        elif fingers == [0, 0, 0, 0, 0]: 
            return "Pause"
        elif fingers == [0, 1, 1, 0, 0]: 
            return "Volume Up"
        elif fingers == [0, 0, 0, 1, 1]: 
            return "Volume Down"
        elif fingers == [0, 0, 0, 0, 1]: 
            return "Next"
        elif fingers == [1, 1, 1, 1, 0]: 
            return "Previous"
        elif fingers == [1, 0, 0, 0, 0]: 
            return "Stop"
        return "Unknown"

    def run(self):
        cap = cv2.VideoCapture(0)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
        mp_draw = mp.solutions.drawing_utils
        last_time = 0
        cooldown = 1.5  # Minimum time between actions

        while self.running:
            ret, img = cap.read()
            if not ret: break
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    fingers = self.get_finger_states(hand)
                    gesture = self.classify_gesture(fingers)
                    mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
                    
                    if time.time() - last_time > cooldown and gesture != self.last_gesture:
                        self.last_gesture = gesture  # Avoid repeating the same gesture
                        print(f"Gesture: {gesture}")
                        
                        # Perform action based on gesture
                        if gesture == "Play" or gesture == "Pause":
                            pyautogui.press('k')
                        elif gesture == "Volume Up":
                            pyautogui.press('up')
                        elif gesture == "Volume Down":
                            pyautogui.press('down')
                        elif gesture == "Next":
                            pyautogui.hotkey('shift', 'n')
                        elif gesture == "Previous":
                            pyautogui.hotkey('shift', 'p')
                        elif gesture == "Stop":
                            pyautogui.press('space')  # Stop playback (toggle play/pause)

                        last_time = time.time()

            cv2.imshow("Gesture Control", img)
            if cv2.waitKey(1) == 27:  # Press ESC to exit
                break

        cap.release()
        cv2.destroyAllWindows()

    def start(self):
        if not self.running:
            with self.lock:
                self.running = True
                self.thread = threading.Thread(target=self.run)
                self.thread.start()

    def stop(self):
        with self.lock:
            self.running = False
        if self.thread:
            self.thread.join()

# Usage example
gesture_recognition = GestureRecognition()
gesture_recognition.start()

# To stop the recognition, you can call gesture_recognition.stop() after use
