// MultiZone GPIO Handler Arduino Sketch
// Handles talker status monitoring and processing control

// Pin definitions
const int TALKER_PINS[] = {2, 3, 4, 5}; // Digital pins for reading talker VAD status
const int PROCESSING_LED_PIN = 13;      // Built-in LED for processing on/off toggle
const int NUM_ZONES = 4;

// State variables
bool processingEnabled = false;
bool talkerStatus[NUM_ZONES] = {false, false, false, false};
unsigned long lastTalkerUpdate = 0;
const unsigned long TALKER_UPDATE_INTERVAL = 100; // Update every 100ms

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Initialize talker input pins
  for (int i = 0; i < NUM_ZONES; i++) {
    pinMode(TALKER_PINS[i], INPUT_PULLUP);
  }

  // Initialize processing LED pin
  pinMode(PROCESSING_LED_PIN, OUTPUT);
  digitalWrite(PROCESSING_LED_PIN, LOW);

  // Send ready signal
  Serial.println("ARDUINO_READY");
}

void loop() {
  // Handle incoming serial commands
  handleSerialCommands();

  // Update talker status at regular intervals
  if (millis() - lastTalkerUpdate >= TALKER_UPDATE_INTERVAL) {
    updateTalkerStatus();
    sendTalkerStatus();
    lastTalkerUpdate = millis();
  }

  // Small delay to prevent excessive CPU usage
  delay(10);
}

void handleSerialCommands() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("PROCESS:")) {
      // Handle processing on/off command
      String value = command.substring(8);
      if (value == "1") {
        processingEnabled = true;
        digitalWrite(PROCESSING_LED_PIN, HIGH);
        Serial.println("PROCESS_ON");
      } else if (value == "0") {
        processingEnabled = false;
        digitalWrite(PROCESSING_LED_PIN, LOW);
        Serial.println("PROCESS_OFF");
      }
    }
    else if (command == "RESET") {
      // Handle reset command
      processingEnabled = false;
      digitalWrite(PROCESSING_LED_PIN, LOW);
      for (int i = 0; i < NUM_ZONES; i++) {
        talkerStatus[i] = false;
      }
      Serial.println("RESET_OK");
    }
    else if (command == "STATUS") {
      // Handle status request
      sendTalkerStatus();
    }
  }
}

void updateTalkerStatus() {
  // Read talker status from GPIO pins
  // Note: Using INPUT_PULLUP, so LOW = active, HIGH = inactive
  for (int i = 0; i < NUM_ZONES; i++) {
    bool pinState = digitalRead(TALKER_PINS[i]);
    talkerStatus[i] = !pinState; // Invert because of pullup
  }
}

void sendTalkerStatus() {
  // Send talker status in expected format: "TALKER:0,1,0,1"
  Serial.print("TALKER:");
  for (int i = 0; i < NUM_ZONES; i++) {
    Serial.print(talkerStatus[i] ? "1" : "0");
    if (i < NUM_ZONES - 1) {
      Serial.print(",");
    }
  }
  Serial.println();
}