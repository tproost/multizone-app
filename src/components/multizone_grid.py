import streamlit as st
from .gpio_handler import get_gpio_handler
from .audio_cue_handler import get_audio_cue_handler
import time
import random


def create_multizone_grid():
    # Initialize session state for active zone (only one can be active)
    if "active_zone" not in st.session_state:
        st.session_state.active_zone = None

    # Initialize session state for Goodix processing - DEFAULT TO TRUE
    if "goodix_processing" not in st.session_state:
        st.session_state.goodix_processing = False

    # Initialize session state for Background noise - DEFAULT TO FALSE
    if "background_noise" not in st.session_state:
        st.session_state.background_noise = False

    # Initialize session state for Background noise - DEFAULT TO FALSE
    if "fe" not in st.session_state:
        st.session_state.fe = False

    # Initialize session state for NE talker - DEFAULT TO FALSE
    if "ne_talker" not in st.session_state:
        st.session_state.ne_talker = False

    # Initialize session state for Audio playback - DEFAULT TO FALSE
    if "audio_playback" not in st.session_state:
        st.session_state.audio_playback = False

    # Initialize GPIO connection state
    if "gpio_connected" not in st.session_state:
        st.session_state.gpio_connected = False

    # Initialize Reaper connection state
    if "audio_connected" not in st.session_state:
        st.session_state.audio_connected = False

    # Initialize artificial talker signals when Arduino is not connected
    if "artificial_talker_status" not in st.session_state:
        st.session_state.artificial_talker_status = [False, False, False, False]

    if "last_artificial_update" not in st.session_state:
        st.session_state.last_artificial_update = time.time()

    # Get GPIO handler
    gpio_handler = get_gpio_handler()
    # Get Audio Cue handler
    try:
        audio_handler = get_audio_cue_handler()
        st.session_state.audio_connected = True
    except Exception as e:
        st.session_state.audio_connected = False
        st.info("Audio connection not established, error: " + str(e))

    # Generate artificial talker signals if not connected to Arduino
    if not st.session_state.gpio_connected:
        current_time = time.time()
        # Update artificial signals every 2-4 seconds randomly
        time_since_update = current_time - st.session_state.last_artificial_update
        if time_since_update >= random.uniform(2.0, 4.0):
            # Randomly change talker status for each zone
            st.session_state.artificial_talker_status = [
                random.choice([True, False]) for _ in range(4)
            ]
            st.session_state.last_artificial_update = current_time

    # Add custom CSS to style buttons as squares
    st.markdown(
        """
    <style>
    div.stButton > button {
        width: 150px !important;
        height: 150px !important;
        border-radius: 8px !important;
        border: 2px solid #ccc !important;
        margin: 10px auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    .talker-indicator {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: inline-block;
        margin-left: 10px;
        border: 2px solid #666;
    }
    .talker-active {
        background-color: #00ff00;
        box-shadow: 0 0 10px #00ff00;
    }
    .talker-inactive {
        background-color: #666;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    def create_zone_square(col, zone_index, zone_name):
        """Helper function to create a clickable zone square."""
        with col:
            # Check if this zone is the active one
            is_active = st.session_state.active_zone == zone_index

            # Get talker status from GPIO or artificial signals (only if processing is ON)
            talker_status = False
            if st.session_state.goodix_processing:  # Only show if processing is ON
                if st.session_state.gpio_connected:
                    zone_talker_statuses = gpio_handler.get_zone_talker_status()
                    if zone_index < len(zone_talker_statuses):
                        talker_status = zone_talker_statuses[zone_index]
                else:
                    # Use artificial signals when Arduino is not connected
                    if zone_index < len(st.session_state.artificial_talker_status):
                        talker_status = st.session_state.artificial_talker_status[
                            zone_index
                        ]

            # Create button content based on state
            if is_active:
                button_label = f"🎧 {zone_name}"
                button_type = "primary"
            else:
                button_label = zone_name
                button_type = "secondary"

            # Only show talker status indicator if Goodix processing is ON
            if st.session_state.goodix_processing:
                talker_class = "talker-active" if talker_status else "talker-inactive"
                talker_html = f'<div class="talker-indicator {talker_class}"></div>'

                # Add connection status indicator
                connection_status = "🔗" if st.session_state.gpio_connected else "📡"

                st.markdown(
                    f'<div style="text-align: center; margin-bottom: 5px;">'
                    f"{zone_name} Talker Status {talker_html} {connection_status}</div>",
                    unsafe_allow_html=True,
                )
            else:
                # Show just the zone name when processing is OFF
                st.markdown(
                    f'<div style="text-align: center; margin-bottom: 5px;">'
                    f"{zone_name}</div>",
                    unsafe_allow_html=True,
                )

            # Create the clickable button
            if st.button(button_label, key=f"btn_{zone_index}", type=button_type):
                # Toggle the active zone
                if st.session_state.active_zone == zone_index:
                    st.session_state.active_zone = None
                else:
                    st.session_state.active_zone = zone_index
                st.rerun()

    # Create a 2x2 grid layout
    col1, col2 = st.columns(2)

    # First row
    create_zone_square(col1, 0, "Driver")
    create_zone_square(col2, 1, "Codriver")

    # Second row
    create_zone_square(col1, 2, "Rear Left")
    create_zone_square(col2, 3, "Rear Right")

    # Add spacing and control buttons
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Control buttons side by side
    col1, col2, col3, col4 = st.columns(4)

    # Goodix processing button
    with col1:
        goodix_status = "ON" if st.session_state.goodix_processing else "OFF"
        goodix_button_type = (
            "primary" if st.session_state.goodix_processing else "secondary"
        )

        if st.button(
            f"Goodix processing {goodix_status}",
            key="goodix_btn",
            type=goodix_button_type,
        ):
            new_status = not st.session_state.goodix_processing
            st.session_state.goodix_processing = new_status

            # Send command to Arduino if connected
            if st.session_state.gpio_connected:
                success = gpio_handler.send_processing_command(new_status)
                if success:
                    st.success(
                        f"Processing {'enabled' if new_status else 'disabled'} on Arduino"
                    )
                else:
                    st.error("Failed to send command to Arduino")
            else:
                # Show artificial feedback when not connected
                st.info(
                    f"Artificial mode: Processing {'enabled' if new_status else 'disabled'}"
                )

            st.rerun()

    # Music button (FE) button
    with col2:
        noise_status = "ON" if st.session_state.fe else "OFF"
        noise_button_type = "primary" if st.session_state.fe else "secondary"

        if st.button(f"Music {noise_status}", key="fe_btn", type=noise_button_type):
            new_fe_status = not st.session_state.fe
            st.session_state.fe = new_fe_status

            # Send background noise command to Reaper if connected
            if st.session_state.audio_connected:
                audio_handler.toggle_content_mute("FE")
                st.success(f"Music {'enabled' if new_fe_status else 'disabled'}")
            else:
                # Show artificial feedback when not connected
                st.info(
                    f"Artificial mode: Music {'enabled' if new_fe_status else 'disabled'}"
                )

            st.rerun()

    # Background noise button
    with col3:
        noise_status = "ON" if st.session_state.background_noise else "OFF"
        noise_button_type = (
            "primary" if st.session_state.background_noise else "secondary"
        )

        if st.button(
            f"Background noise {noise_status}", key="noise_btn", type=noise_button_type
        ):
            new_noise_status = not st.session_state.background_noise
            st.session_state.background_noise = new_noise_status

            # Send background noise command to Reaper if connected
            if st.session_state.audio_connected:
                audio_handler.toggle_content_mute("BGN")
                st.success(
                    f"Background noise {'enabled' if new_noise_status else 'disabled'}"
                )
            else:
                # Show artificial feedback when not connected
                st.info(
                    f"Artificial mode: Background noise {'enabled' if new_noise_status else 'disabled'}"
                )

            st.rerun()

        # NE talker button
        with col4:
            ne_status = "ON" if st.session_state.ne_talker else "OFF"
            ne_button_type = "primary" if st.session_state.ne_talker else "secondary"

            if st.button(f"Talkers {ne_status}", key="ne_btn", type=ne_button_type):
                new_ne_status = not st.session_state.ne_talker
                st.session_state.ne_talker = new_ne_status

                # Send NE talker command to Reaper if connected
                if st.session_state.audio_connected:
                    audio_handler.toggle_content_mute("NE")
                    st.success(
                        f"NE talker {'enabled' if new_ne_status else 'disabled'}"
                    )
                else:
                    # Show artificial feedback when not connected
                    st.info(
                        f"Artificial mode: NE talker {'enabled' if new_ne_status else 'disabled'}"
                    )

                st.rerun()

    # Arduino Connection and Audio Playback Section - moved to bottom and made smaller
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    # Arduino connection in center-left
    with col2:
        if not st.session_state.gpio_connected:
            if st.button(
                "Connect Arduino", key="connect_gpio", help="Connect to Arduino via USB"
            ):
                if gpio_handler.connect():
                    st.session_state.gpio_connected = True
                    st.success("Connected!")
                    st.rerun()
        else:
            status_color = "🟢" if gpio_handler.is_connected else "🔴"
            st.markdown(
                f"<div style='text-align: center; font-size: 12px;'>{status_color} Arduino</div>",
                unsafe_allow_html=True,
            )

            if st.button(
                "Disconnect", key="disconnect_gpio", help="Disconnect from Arduino"
            ):
                gpio_handler.disconnect()
                st.session_state.gpio_connected = False
                st.info("Disconnected")
                st.rerun()

    # Audio playback button in center-right
    with col4:
        if not st.session_state.audio_connected:
            if st.button(
                "Connect Audio",
                key="connect_audio",
                help="Connect to Reaper for audio playback",
            ):
                try:
                    audio_handler = get_audio_cue_handler()
                    st.session_state.audio_connected = True
                    st.success("Connected!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to connect: {e}")
        else:
            # Show audio status when connected
            if not st.session_state.audio_playback:
                # Show connection status and play button
                status_color = "🟢" if st.session_state.audio_connected else "🔴"
                st.markdown(
                    f"<div style='text-align: center; font-size: 12px;'>{status_color} Audio connected</div>",
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Start Audio", key="start_audio", help="Start audio playback"
                ):
                    try:
                        audio_handler.set_ne_loop()
                        audio_handler.start_playback()
                        st.session_state.audio_playback = True
                        st.success("Audio started!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to start audio: {e}")
            else:
                # Show playing status and stop button
                st.markdown(
                    f"<div style='text-align: center; font-size: 12px;'>🎵 Playing</div>",
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Stop Audio", key="stop_audio", help="Stop audio playback"
                ):
                    try:
                        audio_handler.stop_playback()
                        st.session_state.audio_playback = False
                        st.success("Audio stopped!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to stop audio: {e}")

    # Status indicator at the bottom
    status_messages = []

    if not st.session_state.gpio_connected and st.session_state.goodix_processing:
        status_messages.append("📡 Artificial mode - Random talker signals")
    elif not st.session_state.goodix_processing:
        status_messages.append("⏸️ Talker monitoring disabled")

    if st.session_state.background_noise:
        status_messages.append("🔊 Background noise enabled")

    if st.session_state.audio_playback:
        status_messages.append("🎵 Audio playback active")

    if status_messages:
        st.markdown(
            f"<div style='text-align: center; font-size: 10px; color: #666; margin-top: 10px;'>"
            f"{' | '.join(status_messages)}</div>",
            unsafe_allow_html=True,
        )

    # Auto-refresh for real-time updates (only when processing is ON)
    if st.session_state.goodix_processing:
        time.sleep(0.5)  # Refresh every 500ms
        st.rerun()
