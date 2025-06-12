# MultiZone GUI Application

A Streamlit application featuring a multi-zone interactive grid with Arduino GPIO integration and audio cue handling via REAPER.

## 🎯 Features

- 4-zone interactive grid (Driver, Codriver, Rear Left, Rear Right)
- Real-time talker status monitoring
- Arduino GPIO integration via serial communication
- Audio cue handling via REAPER integration
- Goodix processing control
- Background noise control
- Artificial signal simulation when Arduino not connected

## 🚀 Quick Start

### Online Demo
Try the live demo: [MultiZone App](https://multizone-app-tproost.streamlit.app)

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tproost/multizone-app.git
   cd multizone-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Audio Setup (Required for full functionality):**
   - Install REAPER DAW
   - Open a REAPER project file before running the GUI application (see example.rpp)
   - Ensure REAPER track names include the following channel types:
     - **BGN** - Background Noise tracks
     - **NE** - Near End tracks
     - **FE** - Far End tracks

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🎵 Audio Cue Handler

The application integrates with REAPER for audio cue management:

### REAPER Setup Requirements
- REAPER must be running with the project loaded **before** starting the GUI application
- Track naming convention is critical for proper channel identification
- Supported channel content types in track names (mute toggle per type):
  - `BGN` - Background noise channels
  - `NE` - Near end audio channels
  - `FE` - Far end audio channels

### Example Track Names
```
BGN_some_noise
NE_codriver_01
NE_driver
FE_RearLeft_Main
```

## 🔧 Arduino Setup

### Arduino CLI Installation (Optional)

For command-line sketch uploading, install Arduino CLI:

**Windows:**
```bash
# Using Chocolatey
choco install arduino-cli

# Or download from GitHub releases
# https://github.com/arduino/arduino-cli/releases
```

**Setup Arduino CLI:**
```bash
# Initialize configuration
arduino-cli core update-index

# Install Arduino AVR core (for Uno/Nano)
arduino-cli core install arduino:avr

# Check: list connected boards
arduino-cli board list
```

### Manual Arduino Setup

1. Upload the provided Arduino sketch (`arduino_sketch/multizone_gpio.ino`)
2. Connect GPIO pins as defined in the sketch
3. Connect Arduino via USB
4. Use "Connect Arduino" button in the app

### Pin Configuration
- **Talker Inputs:** Digital pins 2, 3, 4, 5
- **Processing Output:** Digital pin 13 (LED)

## 📱 Usage

1. **Audio Setup:** Ensure REAPER is running with proper track naming before starting the application
2. **Zone Selection:** Click any zone button to activate audio processing
3. **Talker Monitoring:** Green dots indicate active talkers (when Goodix processing is ON)
4. **Arduino Connection:** Connect to Arduino via USB for real GPIO monitoring
5. **Artificial Mode:** When Arduino disconnected, shows simulated talker activity

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy using your forked repository

### Other Platforms
- **Railway:** `railway up`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

Found a bug? Please [open an issue](https://github.com/YOUR_USERNAME/multizone-app/issues) with:
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## 🔍 Known improvement points
- Make Arduino GPIO pins configurable

