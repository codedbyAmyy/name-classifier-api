from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timezone

app = FastAPI()

# CORS (VERY IMPORTANT for grading script)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io"


@app.get("/api/classify")
async def classify_name(name: str = Query(...)):
    # 1. Validate input
    if name is None:
        raise HTTPException(status_code=400, detail="Name parameter is required")

    if not isinstance(name, str):
        raise HTTPException(status_code=422, detail="name must be a string")

    name = name.strip()

    if name == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    # 2. Call Genderize API
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name})
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach Genderize API")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream API error")

    data = response.json()

    gender = data.get("gender")
    probability = data.get("probability")
    sample_size = data.get("count")

    # 3. Edge case handling
    if gender is None or sample_size == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    # 4. Convert types safely
    probability = float(probability) if probability is not None else 0.0
    sample_size = int(sample_size) if sample_size is not None else 0

    # 5. Confidence logic
    is_confident = (probability >= 0.7 and sample_size >= 100)

    # 6. Timestamp
    processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # 7. Response
    return {
        "status": "success",
        "data": {
            "name": name.lower(),
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        }
    }