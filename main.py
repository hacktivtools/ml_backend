import os
import io
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from langdetect import detect
from google.cloud import texttospeech

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "W:\HacktivSpace\ml_backend\edza-451010-8c0085628b62.json"

# Mapping language codes to Google TTS voices
LANGUAGE_TO_VOICE = {
    "hi": ("hi-IN", "hi-IN-Wavenet-A"),
    "bn": ("bn-IN", "bn-IN-Wavenet-A"),
    "ta": ("ta-IN", "ta-IN-Wavenet-A"),
    "te": ("te-IN", "te-IN-Wavenet-A"),
    "kn": ("kn-IN", "kn-IN-Wavenet-A"),
    "gu": ("gu-IN", "gu-IN-Wavenet-A"),
    "ml": ("ml-IN", "ml-IN-Wavenet-A"),
    "mr": ("mr-IN", "mr-IN-Wavenet-A"),
    "ur": ("ur-IN", "ur-IN-Wavenet-A"),
    "en": ("en-IN", "en-IN-Wavenet-A"),
}

app = FastAPI()

@app.get("/tts-auto")
def tts_auto(text: str = Query(..., description="Text to convert to speech")):
    try:
        lang_code = detect(text)
        if lang_code not in LANGUAGE_TO_VOICE:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {lang_code}")

        language_code, voice_name = LANGUAGE_TO_VOICE[lang_code]

        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        mp3_stream = io.BytesIO(response.audio_content)

        return StreamingResponse(mp3_stream, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
