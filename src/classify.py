import RPi.GPIO as GPIO
import time
import subprocess
import threading
import json
import websocket

PIR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

BIRDS = ["blackbird", "robin", "pigeon", "wren"]
last_detection = {}

def on_message(ws, message):
    try:
        data = json.loads(message)
        if "result" in data:
            result = data["result"]
            if "classification" in result:
                scores = result["classification"]
                best = max(scores, key=scores.get)
                conf = scores[best]
                if conf > 0.6:
                    print("="*30)
                    print("BIRD: " + best.upper())
                    print("CONFIDENCE: " + str(round(conf*100,1)) + "%")
                    print("BUZZER: Alert!")
                    print("="*30)
    except:
        pass

def on_error(ws, error):
    pass

def on_close(ws, a, b):
    pass

def on_open(ws):
    print("Connected to classifier!")

def start_runner():
    subprocess.Popen(["edge-impulse-linux-runner",
        "--model", "/home/bryank93/birdfeeder.eim"])

print("Starting classifier...")
t = threading.Thread(target=start_runner)
t.daemon = True
t.start()
time.sleep(5)

print("Waiting for motion...")
try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion! Connecting to classifier...")
            ws = websocket.WebSocketApp("ws://192.168.1.189:4912",
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open)
            wst = threading.Thread(target=ws.run_forever)
            wst.daemon = True
            wst.start()
            time.sleep(5)
            ws.close()
            print("Cooling down...")
            time.sleep(3)
        else:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped!")
finally:
    GPIO.cleanup()
