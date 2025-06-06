# MultiZone GUI Application

A Streamlit application featuring a multi-zone interactive grid with Arduino GPIO integration.

## Features

- 4-zone interactive grid (Driver, Codriver, Rear Left, Rear Right)
- Real-time talker status monitoring
- Arduino GPIO integration via serial communication
- Goodix processing control
- Background noise control
- Artificial signal simulation when Arduino not connected

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Arduino Setup

Upload the provided Arduino sketch to monitor GPIO pins and control outputs.

## Deployment

This app can be deployed on:
- Streamlit Cloud
- Heroku
- Railway
- Render