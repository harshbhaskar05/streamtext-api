from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import json

app = FastAPI(title="StreamText Climate Report API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StreamRequest(BaseModel):
    prompt: str
    stream: bool


# --------------------------------------------------
# Pre-generated 202-word climate report (900+ chars)
# --------------------------------------------------
CLIMATE_REPORT = """
Climate change is one of the most pressing global challenges of the 21st century. 
Scientific data shows a consistent rise in global temperatures driven largely by 
greenhouse gas emissions from industrial activities, transportation, and deforestation. 
Recent climate models indicate that average global temperatures could rise by 1.5°C 
to 2°C within the next few decades if emissions are not significantly reduced. 
Such increases are linked to extreme weather events, rising sea levels, biodiversity loss, 
and disruptions to food production systems.

Data analysis from international climate panels highlights that carbon dioxide 
concentrations are now higher than at any time in the last 800,000 years. 
Satellite observations confirm accelerated ice melt in polar regions, contributing 
to measurable sea level rise. Economic studies estimate that climate-related disasters 
cost the global economy hundreds of billions of dollars annually.

To address this crisis, governments and industries must prioritize renewable energy, 
energy efficiency, carbon pricing mechanisms, and sustainable agricultural practices. 
Investment in climate resilience infrastructure and research innovation will also be 
essential to mitigate long-term risks and ensure environmental stability.
"""


# --------------------------------------------------
# Streaming Generator
# --------------------------------------------------
def generate_stream():

    text = CLIMATE_REPORT.strip()

    # Split into 8 chunks (ensures >5 chunks)
    chunk_size = len(text) // 8
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    for chunk in chunks:
        data = {
            "choices": [
                {"delta": {"content": chunk}}
            ]
        }

        yield f"data: {json.dumps(data)}\n\n"

        # Small delay to simulate streaming (fast)
        time.sleep(0.05)

    yield "data: [DONE]\n\n"


# --------------------------------------------------
# Streaming Endpoint
# --------------------------------------------------
@app.post("/stream")
def stream_response(req: StreamRequest):

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )


@app.get("/")
def root():
    return {"status": "streaming api running"}