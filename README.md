# 🎙️ NeuTTS Voice Cloning Engine

A professional, modular voice cloning application using NeuTTS for few-shot voice synthesis. Upload a short audio sample, and the system will clone that voice to speak any text you provide.

## ✨ Features

- **Few-Shot Voice Cloning**: Clone any voice with just 5-15 seconds of audio
- **Instant Voice Generation**: Generate speech in cloned voices in seconds
- **Voice Management**: Save, load, and delete custom voice profiles
- **Speed Control**: Adjust playback speed from 0.5x to 2.0x
- **Smart Text Processing**: Automatic text chunking for optimal generation
- **Progress Tracking**: Real-time progress updates during generation

## 🏗️ Architecture

This project follows a professional modular architecture:

```
Voice_Cloning_Engine/
├── config.py                    # Configuration and constants
├── main.py                      # Application entry point
├── utils/
│   ├── __init__.py
│   └── system_check.py         # eSpeak verification
├── core/
│   ├── __init__.py
│   ├── model_manager.py        # TTS model initialization
│   ├── voice_manager.py        # Voice loading/management
│   ├── text_processor.py       # Text chunking utilities
│   └── speech_generator.py     # Speech generation pipeline
├── ui/
│   ├── __init__.py
│   └── gradio_interface.py     # Gradio UI components
├── samples/                     # Voice samples directory
├── Models/                      # Model files directory
└── requirements.txt             # Python dependencies
```

### Module Responsibilities

- **config.py**: Centralized configuration (paths, model settings, audio parameters)
- **utils/system_check.py**: System dependency verification (eSpeak-NG)
- **core/model_manager.py**: NeuTTS model initialization and management
- **core/voice_manager.py**: Voice operations (load, clone, delete)
- **core/text_processor.py**: Intelligent text chunking with sentence preservation
- **core/speech_generator.py**: TTS generation pipeline with progress tracking
- **ui/gradio_interface.py**: Gradio web interface components
- **main.py**: Application initialization and launch

## 📦 Requirements

### System Requirements

- **OS**: Windows 10/11
- **Python**: 3.9, 3.10, or 3.11 (⚠️ **Not 3.12+**)
- **RAM**: 8 GB minimum (16 GB recommended)
- **Storage**: ~3 GB free space
- **eSpeak-NG**: Required for phonemization

### Software Requirements

- Python 3.9-3.11
- pip (Python package manager)
- eSpeak-NG ([Download](https://github.com/espeak-ng/espeak-ng/releases))

## 🚀 Installation

### Step 1: Install eSpeak-NG

1. Download eSpeak-NG from [GitHub Releases](https://github.com/espeak-ng/espeak-ng/releases)
2. Run the installer (`espeak-ng.msi`)
3. Follow installation prompts (default location recommended)

### Step 2: Set Up Python Environment

```bash
# Navigate to project directory
cd Voice_Cloning_Engine

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: First run will download the NeuTTS model (~1-2 GB) from HuggingFace.

## 🎯 Usage

### Starting the Application

```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate

# Run the application
python main.py
```

The application will:
1. ✓ Verify eSpeak-NG installation
2. ✓ Initialize TTS model
3. ✓ Load available voices
4. ✓ Launch Gradio interface

The UI will open automatically in your browser at `http://localhost:7860`

### Using the Interface

#### Generate Speech Tab

1. **Select Voice**: Choose from available voice profiles
2. **Enter Text**: Type or paste the text to synthesize
3. **Adjust Speed**: Use slider to control playback speed (0.5x - 2.0x)
4. **Generate**: Click "🎙️ Generate Speech"
5. **Listen**: Audio plays automatically when ready
6. **Delete Voice**: Remove unwanted voice profiles with "🗑️ Delete Voice"

#### Clone New Voice Tab

1. **Voice Name**: Enter a unique name for the new voice
2. **Reference Text**: Type the exact text spoken in the audio sample
3. **Upload Audio**: Select a WAV file (5-20 seconds recommended)
4. **Clone**: Click "🧬 Clone Voice"
5. **Use**: New voice appears in the dropdown on the Generate tab

## 🔍 How It Works

### Pipeline Overview

```
Text Input → Text Chunking → TTS Generation (per chunk) → 
Audio Assembly → Speed Adjustment → Final Output
```

### Key Components

1. **Text Processing**
   - Splits text into chunks (max 150 chars)
   - Preserves sentence boundaries
   - Handles long sentences by splitting on commas
   - Maintains punctuation structure

2. **Voice Encoding**
   - Loads reference audio and text
   - Extracts speaker embedding using NeuTTS
   - Caches embeddings as `.pt` files for faster loading

3. **Speech Generation**
   - Processes each text chunk independently
   - Generates audio using NeuTTS model
   - Tracks progress and estimates completion time
   - Assembles chunks with silence padding

4. **Post-Processing**
   - Applies speed adjustment if needed
   - Normalizes audio levels
   - Saves as WAV file

### Model Details

**NeuTTS** is a neural text-to-speech model that:
- Supports few-shot voice cloning
- Requires minimal reference audio (5-15 seconds)
- Generates high-quality, natural-sounding speech
- Runs efficiently on CPU

## ⚡ Performance

### Generation Times (CPU)

| Text Length | Chunks | Estimated Time |
|-------------|--------|----------------|
| Short (1-2 sentences) | 1-2 | 5-10 seconds |
| Medium (paragraph) | 3-5 | 15-25 seconds |
| Long (multiple paragraphs) | 6-10 | 30-60 seconds |

### Optimization Tips

1. **Keep model loaded**: Don't restart the app between generations
2. **Use quality audio**: Clear speech produces better results
3. **Optimal reference length**: 10-15 seconds is ideal
4. **Close other apps**: Free up CPU resources

## 🔧 Troubleshooting

### eSpeak-NG Not Found

**Error**: `Error: espeak-ng not found!`

**Solution**:
1. Install eSpeak-NG from [GitHub Releases](https://github.com/espeak-ng/espeak-ng/releases)
2. Ensure it's in your PATH
3. Restart the application

### Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'neuttsair'`

**Solution**:
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Model Download Issues

**Problem**: Model download fails or times out

**Solution**:
- Check internet connection
- Ensure ~3 GB free disk space
- Try running again (download resumes automatically)

### Audio Quality Issues

**Problem**: Generated voice sounds robotic or distorted

**Solution**:
- Use higher quality reference audio (clear, no background noise)
- Ensure reference audio is 10-15 seconds long
- Match reference text exactly to what's spoken
- Try different reference samples

## 📁 Voice Samples

Voice samples are stored in the `samples/` directory with three files per voice:

- `{voice_name}.txt` - Reference text
- `{voice_name}.wav` - Reference audio
- `{voice_name}.pt` - Cached speaker embedding

You can manually add voices by placing these files in the `samples/` directory.

## 🛠️ Development

### Project Structure Benefits

- **Modularity**: Each component has a single responsibility
- **Maintainability**: Easy to locate and fix bugs
- **Testability**: Components can be tested independently
- **Extensibility**: Add new features without touching existing code
- **Readability**: Clear imports show dependencies

### Adding New Features

1. **New Voice Format**: Modify `voice_manager.py`
2. **Different TTS Model**: Update `model_manager.py`
3. **UI Changes**: Edit `ui/gradio_interface.py`
4. **Configuration**: Update `config.py`


