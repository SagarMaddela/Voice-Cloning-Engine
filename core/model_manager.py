"""
TTS Model Manager for Voice Cloning Engine.

This module handles the initialization and management of the NeuTTS model,
including HuggingFace snapshot resolution and model loading.
"""
import os
import sys
from neuttsair.neutts import NeuTTSAir
from config import (
    MODEL_BACKBONE_LOCAL,
    MODEL_BACKBONE_REPO,
    MODEL_CODEC_REPO,
    MODEL_DEVICE
)


class ModelManager:
    """
    Manages the TTS model lifecycle.
    
    This class handles model initialization, HuggingFace snapshot resolution,
    and provides access to the loaded model instance.
    """
    
    def __init__(self):
        """Initialize the model manager."""
        self.model = None
        self._initialized = False
    
    @staticmethod
    def _resolve_hf_snapshot(root_path: str) -> str:
        """
        Resolve HuggingFace snapshot path from cache structure.
        
        Args:
            root_path: Root path to search for HuggingFace cache
            
        Returns:
            str: Path to the snapshot or original root_path if not found
        """
        try:
            # Check for HuggingFace cache structure
            for name in os.listdir(root_path):
                if name.startswith("models--"):
                    models_dir = os.path.join(root_path, name)
                    snapshots_dir = os.path.join(models_dir, "snapshots")
                    
                    if os.path.isdir(snapshots_dir):
                        for snap in os.listdir(snapshots_dir):
                            snap_path = os.path.join(snapshots_dir, snap)
                            cfg = os.path.join(snap_path, "config.json")
                            
                            if os.path.exists(cfg):
                                print(f"Found model in snapshots: {snap_path}")
                                return snap_path
        except Exception as e:
            print(f"Warning: Error resolving model path: {e}")
        
        return root_path
    
    def initialize_model(self):
        """
        Initialize the NeuTTS model.
        
        This method loads the model from either local directory or HuggingFace,
        resolving snapshot paths as needed.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        if self._initialized:
            print("Model already initialized")
            return True
        
        print("\nInitializing TTS model...")
        
        try:
            # Determine backbone argument
            if os.path.isdir(MODEL_BACKBONE_LOCAL):
                backbone_arg = self._resolve_hf_snapshot(str(MODEL_BACKBONE_LOCAL))
            else:
                backbone_arg = MODEL_BACKBONE_REPO
            
            print(f"Using backbone: {backbone_arg}")
            print(f"Using codec: {MODEL_CODEC_REPO}")
            
            # Initialize NeuTTS model
            self.model = NeuTTSAir(
                backbone_repo=backbone_arg,
                backbone_device=MODEL_DEVICE,
                codec_repo=MODEL_CODEC_REPO,
                codec_device=MODEL_DEVICE,
            )
            
            self._initialized = True
            print("✓ Model initialized successfully")
            return True
            
        except Exception as e:
            print(f"\nError initializing TTS model: {str(e)}")
            return False
    
    def get_model(self):
        """
        Get the initialized model instance.
        
        Returns:
            NeuTTSAir: The initialized model instance
            
        Raises:
            RuntimeError: If model is not initialized
        """
        if not self._initialized or self.model is None:
            raise RuntimeError("Model not initialized. Call initialize_model() first.")
        
        return self.model
    
    def is_initialized(self):
        """
        Check if model is initialized.
        
        Returns:
            bool: True if model is initialized, False otherwise
        """
        return self._initialized
