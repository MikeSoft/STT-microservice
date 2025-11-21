import os
import shutil
import tempfile
import uvicorn
import json
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, Response
import stable_whisper

app = FastAPI(title="Stable Whisper Microservice")

MODEL_SIZE = "large"
print(f"Loading stable-whisper model: {MODEL_SIZE}...")
model = stable_whisper.load_model(MODEL_SIZE)
print("Model loaded.")

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    output_format: str = Form("json"),
    language: str = Form("es"),
    task: str = Form("transcribe"),
    initial_prompt: Optional[str] = Form(None),
    word_timestamps: bool = Form(True),
    regroup: bool = Form(True),
    suppress_silence: bool = Form(True),
    vad: bool = Form(False),
    # Add other parameters as needed from stable_whisper.transcribe
):
    """
    Transcribe an audio file using stable-whisper.
    
    Args:
        file: The audio file to transcribe.
        output_format: The desired output format (json, srt, vtt, ass, tsv, txt). Default is json.
        ... other stable_whisper parameters.
    """
    
    # Validate output format
    valid_formats = ["json", "srt", "vtt", "ass", "tsv", "txt"]
    if output_format not in valid_formats:
        raise HTTPException(status_code=400, detail=f"Invalid output_format. Must be one of {valid_formats}")

    # Create a temporary file to save the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_audio:
        shutil.copyfileobj(file.file, temp_audio)
        temp_audio_path = temp_audio.name

    try:
        # Prepare arguments for transcribe
        transcribe_args = {
            "audio": temp_audio_path,
            "language": language,
            "task": task,
            "initial_prompt": initial_prompt,
            "word_timestamps": word_timestamps,
            "regroup": regroup,
            "suppress_silence": suppress_silence,
            "vad": vad
        }
        
        # Run transcription
        result = model.transcribe(**transcribe_args)
        
        # Handle output format
        if output_format == "json":
            # Use save_as_json logic but return content directly
            # We can use result.to_dict() or save to temp file and read back if specific formatting is needed
            # The user requested "save_as_json por defecto", which usually implies the structure of that file.
            # save_as_json saves the result.to_dict() to a file.
            return JSONResponse(content=result.to_dict())
            
        elif output_format == "srt":
            content = result.to_srt_vtt(filepath=None, vtt=False)
            return Response(content=content, media_type="text/plain")
            
        elif output_format == "vtt":
            content = result.to_srt_vtt(filepath=None, vtt=True)
            return Response(content=content, media_type="text/vtt")
            
        elif output_format == "ass":
            content = result.to_ass(filepath=None)
            return Response(content=content, media_type="text/plain")
            
        elif output_format == "tsv":
            content = result.to_tsv(filepath=None)
            return Response(content=content, media_type="text/tab-separated-values")
            
        elif output_format == "txt":
            content = result.to_txt(filepath=None)
            return Response(content=content, media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Clean up the temporary audio file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=33000)
