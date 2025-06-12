import reapy_boost as rpr
import os
import time


class AudioCueHandler:
    """
    Class to handle audio cues for the Reaper communication.
    """

    AVAILABLE_CONTENT_TYPES = [
        "NE",
        "FE",
        "BGN",
    ]

    def __init__(self):
        """Initialize the AudioCueHandler and configure Reaper."""
        print("Configuring Reaper...")

        # Configure Reaper
        rpr.configure_reaper()
        os.environ["no_proxy"] = "localhost"

        if not self._verify_reaper_connection():
            raise ConnectionError(
                "Failed to connect to Reaper. Make sure Reaper is running prior to opening this GUI.\n"
                "For setup: Have ReaScript API enabled,"
                "follow steps on https://github.com/RomeoDespres/reapy/issues/103"
            )

        self.track_names = [track.name for track in self.project.tracks]
        print(f"✓ Found {len(self.track_names)} tracks: {self.track_names}")

        # Stop playback if it was running
        self.project.mute_all_tracks()
        self.project.unselect_all_tracks()
        self.project.unsolo_all_tracks()
        if not self.project.is_stopped:
            self.project.stop()

        # Mute all channels
        print("✓ Playback stopped, all channels muted an un-soloed.")
        print("✓ Reaper configured successfully")

    def _verify_reaper_connection(self):
        """Verify that Reaper is properly configured and accessible."""
        try:
            # Test basic Reaper functionality
            rpr.print("Testing Reaper connection...")

            # Check if we can access current project
            self.project = rpr.Project()

            print(f"✓ Reaper configured successfully")
            print(f"✓ Project: {self.project.name}")

            return True

        except Exception as e:
            print(f"✗ Reaper verification failed: {e}")
            return False

    def set_ne_loop(self):
        """Set the NE loop for the current project."""
        # Find time to set loop length to, based on NE track content
        loop_end_time = 0
        for track in self.project.tracks:
            if "NE" in track.name:
                if len(track.items) > 0:
                    # Get the maximum position + length of items in NE track
                    loop_end_time = max(
                        max([item.position + item.length for item in track.items]),
                        loop_end_time,
                    )
        loop_end_time = loop_end_time + 1

        # Set loop points
        time_selection = self.project.time_selection
        time_selection.start = 0
        time_selection.end = loop_end_time

        # Enable loop mode
        self.project.cursor_position = time_selection.start
        time_selection.loop()
        print(f"✓ NE loop set from 0 to {loop_end_time} seconds.")

    def start_playback(self):
        """Start playback of the current project."""
        self.project.play()

    def stop_playback(self):
        """Stop playback of the current project."""
        self.project.stop()

    def toggle_content_mute(self, content_type: str = None):
        """Toggle mute for specific content type for playback."""
        if content_type not in self.AVAILABLE_CONTENT_TYPES:
            raise ValueError(
                f"Invalid content type: {content_type}. Available types: {self.AVAILABLE_CONTENT_TYPES}"
            )

        # Mute or unmute the specified content type
        for track in self.project.tracks:
            if content_type in track.name:
                if track.is_muted:
                    track.unmute()
                else:
                    track.mute()
                print(f"Toggled mute for track: {track.name}")


# Global audio handler instance
_audio_handler = None


def get_audio_cue_handler() -> AudioCueHandler:
    """Get or create the global GPIO handler instance."""
    global _audio_handler
    if _audio_handler is None:
        _audio_handler = AudioCueHandler()
    return _audio_handler


def main():
    """Main function to demonstrate AudioCueHandler usage."""
    print("=== AudioCueHandler Usage Example ===\n")

    # Create an instance of AudioCueHandler
    print("1. Connecting to Reaper...")
    audio_handler = AudioCueHandler()

    # Example 2: Start playback
    print("2. Set loop and start playback...")
    audio_handler.set_ne_loop()
    audio_handler.start_playback()

    # Example 4: Unmute content type
    audio_handler.toggle_content_mute("NE")

    # Example 3: Wait for 4 seconds while audio plays
    print("3. Waiting for 4 seconds...")
    time.sleep(4)
    print("4. Done waiting.")

    # Example 5: Stop playback
    print("5. Stopping audio playback...")
    audio_handler.stop_playback()
    print()

    print("=== Example completed ===")


if __name__ == "__main__":
    main()
