"""
Voice Manager for Voice Cloning Engine.

This module handles all voice-related operations including loading,
cloning, and deleting voice samples.
"""
import os
import torch
import shutil
import gradio as gr
from pathlib import Path
from config import SAMPLES_DIR


class VoiceManager:
    """
    Manages voice samples and operations.
    
    This class handles loading voices from the samples directory,
    cloning new voices, and deleting existing voices.
    """
    
    def __init__(self, tts_model):
        """
        Initialize the voice manager.
        
        Args:
            tts_model: The initialized NeuTTS model instance
        """
        self.tts_model = tts_model
        self.voices = {"samples": {}}
        self.load_voices()
    
    def load_voices(self):
        """
        Load all available voices from the samples directory.
        
        Scans the samples directory for voice files (txt + wav/pt pairs)
        and populates the voices dictionary.
        """
        self.voices = {"samples": {}}
        
        # Ensure samples directory exists
        SAMPLES_DIR.mkdir(exist_ok=True)
        
        # Scan for voice files
        for name in os.listdir(SAMPLES_DIR):
            if name.endswith(".txt"):
                base = os.path.splitext(name)[0]
                txt_path = SAMPLES_DIR / f"{base}.txt"
                wav_path = SAMPLES_DIR / f"{base}.wav"
                pt_path = SAMPLES_DIR / f"{base}.pt"
                
                # Check if we have both text and audio/embedding
                if txt_path.exists() and (wav_path.exists() or pt_path.exists()):
                    audio_or_pt = wav_path if wav_path.exists() else pt_path
                    self.voices["samples"][base] = (str(txt_path), str(audio_or_pt))
        
        print(f"Loaded {len(self.voices['samples'])} voices")
    
    def get_voice_list(self):
        """
        Get list of available voice names.
        
        Returns:
            list: List of voice names
        """
        return list(self.voices["samples"].keys())
    
    def voice_exists(self, voice_name):
        """
        Check if a voice exists.
        
        Args:
            voice_name: Name of the voice to check
            
        Returns:
            bool: True if voice exists, False otherwise
        """
        return voice_name in self.voices["samples"]
    
    def load_reference(self, voice_name):
        """
        Load reference text and codes for a voice.
        
        Args:
            voice_name: Name of the voice to load
            
        Returns:
            tuple: (reference_text, reference_codes)
            
        Raises:
            ValueError: If voice not found
        """
        if not self.voice_exists(voice_name):
            raise ValueError(f"Voice '{voice_name}' not found")
        
        txt_path, audio_or_pt = self.voices["samples"][voice_name]
        
        # Load reference text
        with open(txt_path, "r") as f:
            ref_text = f.read().strip()
        
        # Load or encode reference codes
        if audio_or_pt.endswith(".pt"):
            ref_codes = torch.load(audio_or_pt)
        else:
            ref_codes = self.tts_model.encode_reference(audio_or_pt)
        
        return ref_text, ref_codes
    
    def clone_voice(self, new_name, ref_text, audio_file):
        """
        Clone a new voice from reference audio.
        
        Args:
            new_name: Name for the new voice
            ref_text: Reference text (what is spoken in the audio)
            audio_file: Path to reference audio file
            
        Returns:
            tuple: (status_message, gradio_update_dict)
        """
        try:
            # Input validations
            if not new_name or not new_name.strip():
                return "❌ Error: New Voice name cannot be empty.", gr.update()
            
            if not ref_text or not ref_text.strip():
                return "❌ Error: Reference text cannot be empty.", gr.update()
            
            if not audio_file:
                return "❌ Error: No reference audio file provided.", gr.update()
            
            if self.voice_exists(new_name):
                return f"❌ Error: Voice '{new_name}' already exists. Please choose a different name.", gr.update()
            
            # Ensure samples directory exists
            SAMPLES_DIR.mkdir(exist_ok=True)
            
            # Define file paths
            txt_path = SAMPLES_DIR / f"{new_name}.txt"
            wav_path = SAMPLES_DIR / f"{new_name}.wav"
            pt_path = SAMPLES_DIR / f"{new_name}.pt"
            
            # Save reference text
            with open(txt_path, "w") as f:
                f.write(ref_text.strip())
            
            # Copy audio file
            shutil.copy(audio_file, wav_path)
            
            # Encode reference
            ref_codes = self.tts_model.encode_reference(str(wav_path))
            torch.save(ref_codes, pt_path)
            
            # Add to voices dictionary
            self.voices["samples"][new_name] = (str(txt_path), str(pt_path))
            
            return (
                f"✅ Voice '{new_name}' cloned and saved successfully!",
                gr.update(choices=self.get_voice_list(), value=new_name)
            )
            
        except Exception as e:
            return f"❌ Error cloning voice: {e}", gr.update()
    
    def delete_voice(self, voice_name):
        """
        Delete a voice and its associated files.
        
        Args:
            voice_name: Name of the voice to delete
            
        Returns:
            tuple: (status_message, gradio_update_dict)
        """
        try:
            if not self.voice_exists(voice_name):
                return f"❌ Voice '{voice_name}' not found!", gr.update()
            
            # Define file paths
            txt_path = SAMPLES_DIR / f"{voice_name}.txt"
            wav_path = SAMPLES_DIR / f"{voice_name}.wav"
            pt_path = SAMPLES_DIR / f"{voice_name}.pt"
            
            # Remove files if they exist
            for path in [txt_path, wav_path, pt_path]:
                if path.exists():
                    path.unlink()
            
            # Remove from voices dictionary
            del self.voices["samples"][voice_name]
            
            # Select new voice if available
            remaining_voices = self.get_voice_list()
            new_selected = remaining_voices[0] if remaining_voices else None
            
            return (
                f"✅ Voice '{voice_name}' deleted successfully!",
                gr.update(choices=remaining_voices, value=new_selected)
            )
            
        except Exception as e:
            return f"❌ Error deleting voice: {e}", gr.update()
