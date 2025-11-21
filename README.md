# STT Microservice

This is a lightweight Speech-to-Text service powered by OpenAI's Whisper (stable-whisper). It converts audio files into json or subtitles. It extracts phrases with word-level timestamps, making it ideal for generating video subtitles.

## How to Run

### Using Docker (Recommended)
1. **Build:** `make build`
2. **Run:** `make run`

The service runs on port `33000`.

### Manual Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `python main.py`

## Usage

Send a **POST** request to `/transcribe` with your audio file.

**Parameters:**
- `file`: Audio file (required)
- `language`: Language code (e.g., `en`, `es`). Default: `es`
- `output_format`: `json`, `srt`, `vtt`, `txt`. Default: `json`

### Example

```bash
curl -X POST -F "file=@recording.mp3" http://localhost:33000/transcribe
```
