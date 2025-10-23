"""
Microphone Permission Initializer
Requests user permission and initializes microphone access
"""

import pyaudio
import sys


class MicrophoneInitializer:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.is_initialized = False

    def request_permission(self):
        """Ask user for microphone permission"""
        print("\n" + "="*60)
        print("<� MICROPHONE ACCESS REQUEST")
        print("="*60)
        print("\nThis application would like to access your microphone.")
        print("\nPermissions needed:")
        print("Record audio from your microphone")
        print("Process audio input in real-time")
        print("\nYour privacy: Audio is only processed while this app is running.")
        print("="*60)

        while True:
            response = input("\nAllow microphone access? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'")

    def initialize_microphone(self):
        """Initialize the microphone after permission is granted"""
        try:
            print("\nInitializing microphone...")
            self.audio = pyaudio.PyAudio()

            # Get default input device info
            default_device = self.audio.get_default_input_device_info()
            print(f"Found microphone: {default_device['name']}")

            # Test microphone access
            print("Testing microphone access...")
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )

            # Read a small sample to verify it works
            self.stream.read(1024)

            print("Microphone test successful!")
            self.is_initialized = True

            return True

        except Exception as e:
            print(f"\nL Error initializing microphone: {str(e)}")
            print("\nPossible solutions:")
            print("Check if your microphone is properly connected")
            print("Verify microphone is not being used by another application")
            print("Check system audio settings")
            return False

    def cleanup(self):
        """Clean up resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        print("\n Microphone access closed")

    def start(self):
        """Main initialization flow"""
        # Request permission
        if not self.request_permission():
            print("\nL Microphone access denied")
            print("The application cannot function without microphone access.")
            return False

        # Initialize microphone
        print("\nPermission granted!")
        if not self.initialize_microphone():
            return False

        print("\n" + "="*60)
        print(" MICROPHONE READY")
        print("="*60)
        print("\nYour microphone is now active and ready to use.")
        print("Press Ctrl+C to stop and close microphone access.")
        print("="*60 + "\n")

        return True


def main():
    """Main function to run the microphone initializer"""
    initializer = MicrophoneInitializer()

    try:
        if initializer.start():
            # Keep the program running to maintain microphone access
            print("Microphone is active... (waiting)")
            input("Press Enter to close microphone access...")
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n Interrupted by user")

    except Exception as e:
        print(f"\nL Unexpected error: {str(e)}")

    finally:
        initializer.cleanup()


if __name__ == "__main__":
    main()
