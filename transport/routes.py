from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime, timezone


router = APIRouter()

GENDERIZE_URL = "https://api.genderize.io"

@router.get("/api/classify")
async def classify_name(name: str = Query(...)):
    if not name or name.strip() == "":
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Name query parameter is required"})
    if not isinstance(name, str):
        raise HTTPException(status_code=422, detail={"status": "error", "message": "Name must be a string"})

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name})

        if response.status_code != 200:
            return JSONResponse(status_code=502, content={"status": "error", "message": "External API error"})

        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        if gender is None or count == 0:
            return JSONResponse(status_code=400, content={"status": "error", "message": "No prediction available for the provided name"})
        
        sample_size = count
        is_confident = probability >= 0.7 and sample_size >= 100
        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return{
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }
    except httpx.RequestError:
        return JSONResponse(status_code=502, content={"status": "error", "message": "Failed to reach external API"})
    except Exception:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Internal server error"})