import cv2
import time
import requests

# Roboflow API Details
DATASET_SLUG = "smart-ambulance-detection"
VERSION_NUMBER = "2"
API_KEY = "efkLgOaUl3bbYFRw5CoE"
API_URL = f"https://detect.roboflow.com/{DATASET_SLUG}/{VERSION_NUMBER}?api_key={API_KEY}"

# Telegram Bot API Configuration
TELEGRAM_BOT_TOKEN = "8188693770:AAGXwAqdQKeh6G1piOGj7k3-z2wzXXz99Gs"
CHAT_ID = "5766280369"

def send_telegram_notification(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_url, json=payload)

def check_for_ambulance(image_path, confidence_threshold=0.6):
    with open(image_path, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
    
    if response.status_code == 200:
        result = response.json()
        predictions = result.get("predictions", [])
        for prediction in predictions:
            if "ambulance" in prediction.get("class", "").lower() and prediction.get("confidence", 0) >= confidence_threshold:
                send_telegram_notification("🚑 Ambulance detected!")
                return True
    return False

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Live Video Feed", frame)

    if time.time() - start_time >= 5:
        frame_filename = "frame.jpg"
        cv2.imwrite(frame_filename, frame)
        if check_for_ambulance(frame_filename):
            print("🚑 Ambulance detected!")
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
