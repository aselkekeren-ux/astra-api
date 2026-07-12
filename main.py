import os
import shutil
import openai
import replicate
from fastapi import FastAPI
from pydantic import BaseModel
from elevenlabs.client import ElevenLabs

app = FastAPI()

class AstraReq(BaseModel):
    komut: str

@app.post("/astra")
async def astra_islem(req: AstraReq):
    # Anahtarları sunucu ayarlarından çeker
    client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
    
    # 1. Beyin
    response = client.chat.completions.create(model="anthropic/claude-3.5-sonnet", messages=[{"role": "user", "content": req.komut}])
    cevap = response.choices[0].message.content
    
    # 2. Ses
    eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = eleven.generate(text=cevap, voice="Brian", model="eleven_multilingual_v2")
    with open("cevap.mp3", "wb") as f:
        for chunk in audio: f.write(chunk)
    
    # 3. Dosya ve Zip
    with open("cevap.txt", "w") as f: f.write(cevap)
    shutil.make_archive("astra_cikti", 'zip', '.')
    
    return {"durum": "Hazır", "cevap": cevap}
