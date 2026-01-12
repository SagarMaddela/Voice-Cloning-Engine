"""
Voice Cloning Engine - Main Entry Point

This is the main application file that initializes all components
and launches the Gradio interface.
"""
import sys
from utils.system_check import verify_system_requirements
from core.model_manager import ModelManager
from core.voice_manager import VoiceManager
from core.speech_generator import SpeechGenerator
from ui.gradio_interface import create_interface
from config import (
    SERVER_NAME,
    SERVER_PORT,
    SHARE_GRADIO,
    OPEN_BROWSER,
    SHOW_ERROR
)


def main():
    """
    Main application entry point.
    
    This function:
    1. Verifies system requirements (eSpeak)
    2. Initializes the TTS model
    3. Loads available voices
    4. Creates the speech generator
    5. Builds and launches the Gradio interface
    """
    print("=" * 60)
    print("Voice Cloning Engine - Starting Up")
    print("=" * 60)
    
    # Step 1: Verify system requirements
    print("\n[1/5] Verifying system requirements...")
    if not verify_system_requirements():
        sys.exit(1)
    
    # Step 2: Initialize TTS model
    print("\n[2/5] Initializing TTS model...")
    model_manager = ModelManager()
    if not model_manager.initialize_model():
        print("\nFailed to initialize model. Exiting...")
        sys.exit(1)
    
    # Step 3: Load voices
    print("\n[3/5] Loading available voices...")
    voice_manager = VoiceManager(model_manager.get_model())
    print(f"✓ Loaded {len(voice_manager.get_voice_list())} voices")
    
    # Step 4: Create speech generator
    print("\n[4/5] Initializing speech generator...")
    speech_generator = SpeechGenerator(
        model_manager.get_model(),
        voice_manager
    )
    print("✓ Speech generator ready")
    
    # Step 5: Create and launch interface
    print("\n[5/5] Building user interface...")
    app = create_interface(voice_manager, speech_generator)
    print("✓ Interface ready")
    
    print("\n" + "=" * 60)
    print("Launching application...")
    print("=" * 60)
    
    # Launch Gradio interface
    app.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        share=SHARE_GRADIO,
        inbrowser=OPEN_BROWSER,
        show_error=SHOW_ERROR
    )


if __name__ == "__main__":
    main()
