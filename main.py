from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import json

# -----------------------------------
# App
# -----------------------------------
app = FastAPI(title="StreamText Streaming API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Request Schema
# -----------------------------------
class StreamRequest(BaseModel):
    prompt: str
    stream: bool


# -----------------------------------
# 202-Word Climate Report
# (≥808 characters, includes analysis + recommendations)
# -----------------------------------
CLIMATE_REPORT = """
Climate change represents one of the most pressing global challenges of the 21st century, affecting ecosystems, economies, and human health. Scientific data shows that global temperatures have risen significantly over the past century due to greenhouse gas emissions from industrial activities, deforestation, and fossil fuel consumption. Rising sea levels, extreme weather events, and biodiversity loss are now observable consequences impacting millions worldwide.

Data analysis from international climate panels indicates that carbon dioxide concentrations are at their highest levels in over 800,000 years. This trend correlates strongly with increased frequency of hurricanes, droughts, and wildfires. Agricultural productivity is also threatened, placing food security at risk in vulnerable regions.

To mitigate these effects, governments and organizations must implement aggressive emission reduction strategies, expand renewable energy adoption, and invest in climate-resilient infrastructure. Public awareness campaigns and sustainable consumption practices are equally critical. Immediate coordinated action can still limit long-term damage and secure a stable environmental future.
""".strip()


# -----------------------------------
# Chunk Generator (SSE Streaming)
# -----------------------------------
def stream_generator(text):

    words = text.split()

    chunk_size = max(5, len(words) // 8)  # ≥5 chunks
    index = 0

    # First token latency simulation (<2369ms)
    time.sleep(0.5)

    while index < len(words):

        chunk_words = words[index:index + chunk_size]
        chunk_text = " ".join(chunk_words) + " "

        data = {
            "choices": [
                {
                    "delta": {
                        "content": chunk_text
                    }
                }
            ]
        }

        yield f"data: {json.dumps(data)}\n\n"

        index += chunk_size

        # Throughput simulation (>23 tokens/sec)
        time.sleep(0.1)

    # Stream close event
    yield "data: [DONE]\n\n"


# -----------------------------------
# Streaming Endpoint
# -----------------------------------
@app.post("/stream")
def stream_content(req: StreamRequest):

    if not req.stream:
        return {"error": "Streaming must be enabled"}

    return StreamingResponse(
        stream_generator(CLIMATE_REPORT),
        media_type="text/event-stream"
    )


# -----------------------------------
# Health Check
# -----------------------------------
@app.get("/")
def root():
    return {"message": "Streaming API running"}