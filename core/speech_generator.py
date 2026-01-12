"""
Speech Generator for Voice Cloning Engine.

This module handles the speech generation pipeline including chunk processing,
progress tracking, and audio post-processing.
"""
import time
import numpy as np
import soundfile as sf
from core.text_processor import split_text_into_chunks
from config import SAMPLE_RATE, SILENCE_DURATION, TEMP_OUTPUT_PATH


class SpeechGenerator:
    """
    Manages the speech generation pipeline.
    
    This class orchestrates the TTS generation process including text chunking,
    chunk processing, progress tracking, and audio assembly.
    """
    
    def __init__(self, tts_model, voice_manager):
        """
        Initialize the speech generator.
        
        Args:
            tts_model: The initialized NeuTTS model instance
            voice_manager: The voice manager instance
        """
        self.tts_model = tts_model
        self.voice_manager = voice_manager
    
    @staticmethod
    def process_chunk(chunk, ref_codes, ref_text, tts_model):
        """
        Process a single chunk of text and return the audio.
        
        Args:
            chunk: Text chunk to process
            ref_codes: Reference voice codes
            ref_text: Reference text
            tts_model: TTS model instance
            
        Returns:
            numpy.ndarray: Generated audio or None if error
        """
        try:
            return tts_model.infer(chunk, ref_codes, ref_text)
        except Exception as e:
            # Swallow individual chunk errors and return None
            return None
    
    @staticmethod
    def estimate_generation_time(num_chunks):
        """
        Estimate the generation time based on number of chunks.
        
        Args:
            num_chunks: Number of text chunks
            
        Returns:
            float: Estimated time in seconds
        """
        # Assuming average of 3 seconds per chunk plus overhead
        return num_chunks * 3 + 2
    
    @staticmethod
    def format_time(seconds):
        """
        Format seconds into a readable time string.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            str: Formatted time string
        """
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds:.1f} seconds"
    
    @staticmethod
    def _apply_speed_adjustment(audio, speed):
        """
        Apply speed adjustment to audio.
        
        Args:
            audio: Input audio array
            speed: Speed multiplier (0.5 to 2.0)
            
        Returns:
            numpy.ndarray: Speed-adjusted audio
        """
        if speed == 1.0:
            return audio
        
        target_length = int(len(audio) / speed)
        indices = np.round(np.linspace(0, len(audio) - 1, target_length)).astype(int)
        return audio[indices]
    
    def generate_speech(self, text, voice_name, speed=1.0):
        """
        Generate speech from text using specified voice.
        
        This is a generator function that yields progress updates and final audio.
        
        Args:
            text: Input text to synthesize
            voice_name: Name of the voice to use
            speed: Speed multiplier (0.5 to 2.0)
            
        Yields:
            tuple: (progress, audio_path, status_message, delete_status)
        """
        try:
            # Input validations
            if not text or not text.strip():
                yield 0, None, "❌ Error: Input text cannot be empty.", None
                return
            
            if not voice_name:
                yield 0, None, "❌ Error: No voice selected. Please select a voice.", None
                return
            
            if not self.voice_manager.voice_exists(voice_name):
                yield 0, None, f"❌ Error: Voice '{voice_name}' not found.", None
                return
            
            start_time = time.time()
            
            # Load reference only once
            yield 10, None, "Loading voice reference...", None
            ref_text, ref_codes = self.voice_manager.load_reference(voice_name)
            
            # Split text into smaller chunks for better processing
            chunks = split_text_into_chunks(text)
            total_chunks = len(chunks)
            
            if total_chunks == 0:
                raise ValueError("No text to process")
            
            # Estimate total time
            estimated_time = self.estimate_generation_time(total_chunks)
            status = f"Estimated time to completion: {self.format_time(estimated_time)}\nProcessing {total_chunks} chunks..."
            yield 15, None, status, None
            
            # Process each chunk and store with its index
            chunk_results = []
            for i, chunk in enumerate(chunks, 1):
                # Update progress
                progress = int(15 + (75 * i / total_chunks))
                
                # Calculate and show time statistics
                elapsed_time = time.time() - start_time
                if i > 1:
                    avg_time_per_chunk = elapsed_time / (i - 1)
                    remaining_chunks = total_chunks - (i - 1)
                    estimated_remaining = avg_time_per_chunk * remaining_chunks
                    status = (
                        f"Processing chunk {i}/{total_chunks}\n"
                        f"Progress: {progress}% complete\n"
                        f"Est. remaining: {self.format_time(estimated_remaining)}"
                    )
                else:
                    status = f"Processing chunk {i}/{total_chunks}\nProgress: {progress}% complete"
                
                yield progress, None, status, None
                
                # Generate audio for this chunk
                chunk_wav = self.process_chunk(chunk, ref_codes, ref_text, self.tts_model)
                if chunk_wav is not None:
                    # Store chunk with its index to maintain order
                    chunk_results.append((i-1, chunk_wav))
            
            if not chunk_results:
                raise ValueError("Failed to generate any audio")
            
            # Update status for final processing
            yield 90, None, "Finalizing audio...\nOrdering and combining chunks...", None
            
            # Sort chunks by their original index and extract the audio data
            chunk_results.sort(key=lambda x: x[0])  # Sort by index
            processed_chunks = [chunk[1] for chunk in chunk_results]  # Extract audio data in order
            
            # Create silence once
            silence = np.zeros(int(SAMPLE_RATE * SILENCE_DURATION))
            
            # Concatenate all chunks with silence in between
            all_wav = processed_chunks[0]
            for chunk_wav in processed_chunks[1:]:
                all_wav = np.concatenate([all_wav, silence, chunk_wav])
            
            # Apply speed adjustment if needed
            if speed != 1.0:
                all_wav = self._apply_speed_adjustment(all_wav, speed)
            
            # Save the final audio
            sf.write(str(TEMP_OUTPUT_PATH), all_wav, SAMPLE_RATE)
            
            # Calculate and show total time taken
            total_time = time.time() - start_time
            final_status = f"✅ Generation complete!\nTotal time: {self.format_time(total_time)}"
            
            yield 100, str(TEMP_OUTPUT_PATH), final_status, None
            
        except Exception as e:
            error_status = f"❌ Error generating speech: {str(e)}"
            yield 0, None, error_status, None
