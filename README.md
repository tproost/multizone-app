# MultiZone GUI Application

A Streamlit application featuring a multi-zone interactive grid with Arduino GPIO integration.

## 🎯 Features

- 4-zone interactive grid (Driver, Codriver, Rear Left, Rear Right)
- Real-time talker status monitoring
- Arduino GPIO integration via serial communication
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

3. Run the app:
   ```bash
   streamlit run app.py
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

**macOS:**
```bash
# Using Homebrew
brew install arduino-cli

# Or using curl
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
```

**Linux:**
```bash
# Using curl
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Or download binary from GitHub releases
```

**Setup Arduino CLI:**
```bash
# Initialize configuration
arduino-cli core update-index

# Install Arduino AVR core (for Uno/Nano)
arduino-cli core install arduino:avr

# List connected boards
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

1. **Zone Selection:** Click any zone button to activate audio processing
2. **Talker Monitoring:** Green dots indicate active talkers (when Goodix processing is ON)
3. **Arduino Connection:** Connect via USB for real GPIO monitoring
4. **Artificial Mode:** When Arduino disconnected, shows simulated talker activity

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy using your forked repository

### Other Platforms
- **Railway:** `railway up`
- **Render:** Deploy as web service
- **Heroku:** Use provided `Dockerfile`

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
- Make Arduino COM port configurable
- Make Arduino GPIO pins configurable

