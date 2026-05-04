import RPi.GPIO as GPIO
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2
import numpy as np
import time

# ── GPIO Setup ──────────────────────────────────────────────
PIR_PIN    = 4   # GPIO 4,  physical pin 7
BUZZER_PIN = 17  # GPIO 17, physical pin 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN,    GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

# ── Load TFLite Model ────────────────────────────────────────
interpreter = tflite.Interpreter(model_path="models/bird_classifier.tflite")
interpreter.allocate_tensors()
input_details  = interpreter.get_input_details()
output_details = interpreter.get_output_details()

LABELS   = ["blackbird", "pigeon", "robin", "wren"]
UNWANTED = {"pigeon", "blackbird"}

# ── Camera Setup ─────────────────────────────────────────────
camera = Picamera2()
camera.configure(camera.create_still_configuration(
    main={"size": (96, 96), "format": "RGB888"}
))
camera.start()
time.sleep(2)

def classify_image():
    frame = camera.capture_array()
    img   = frame.astype(np.float32) / 255.0
    img   = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details<sup>0</sup>['index'], img)
    interpreter.invoke()

    output     = interpreter.get_tensor(output_details<sup>0</sup>['index'])<sup>0</sup>
    species    = LABELS[np.argmax(output)]
    confidence = float(np.max(output))
    return species, confidence

# ── Main Loop ────────────────────────────────────────────────
print("Bird Classifier Running — waiting for motion...")
try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected! Capturing image...")
            species, confidence = classify_image()
            print(f"Result: {species} (confidence: {confidence:.2f})")

            if species in UNWANTED and confidence > 0.6:
                print(f"UNWANTED species — activating buzzer!")
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
            else:
                print(f"WANTED species ({species}) — no action.")

            time.sleep(3)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    camera.stop()
    GPIO.cleanup()
