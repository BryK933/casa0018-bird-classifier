# CASA0018: Real-Time Bird Species Classifier

## Overview
A Raspberry Pi 4 that detects birds at a window feeder using a PIR motion 
sensor, classifies the species (Blackbird, Pigeon, Robin, Wren) using a 
MobileNetV2 TFLite model trained on Edge Impulse, and sounds a buzzer to 
deter unwanted species (pigeon, blackbird).

## Hardware
- Raspberry Pi 4 (4GB RAM)
- Raspberry Pi Camera Module v2
- PIR Motion Sensor HC-SR501 — GPIO 4 (Physical Pin 7)
- Active Buzzer — GPIO 17 (Physical Pin 11)
- Half-size Breadboard
- Anker USB-C Power Bank
- Window-mounted acrylic feeder

## Wiring Diagram
![Wiring](docs/images/wiring_diagram.png)

## Model
- Platform: Edge Impulse
- Architecture: MobileNetV2 (TFLite, int8 quantised)
- Input: 96x96 RGB
- Classes: Blackbird, Pigeon, Robin, Wren
- Validation accuracy: 84.0%
- Deployment accuracy: ~70%

## How to Run
1. Clone this repo onto your Raspberry Pi
2. Install dependencies: pip install -r requirements.txt
3. Copy your model to /models/bird_classifier.tflite
4. Run: python3 src/classify.py

## Results
See results/ folder for terminal output screenshots and evidence.

## Key Findings
- Background removal improved accuracy by 17.3 percentage points (66.7% to 84.0%)
- Event-driven PIR trigger conserves processing resources
- Active buzzer required instead of passive for simple GPIO HIGH signal
- Quantised TFLite model reduced to 1.5MB for edge deployment

## Author
Bryan Kinane — MSc Connected Environments, UCL
CASA0018 Deep Learning for Sensor Networks 2025/2026

