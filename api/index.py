from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    regions: List[str]
    threshold_ms: int

# Your data embedded in the code
data = [
    {"region": "apac", "service": "recommendations", "latency_ms": 140.96, "uptime_pct": 97.466, "timestamp": 20250301},
    {"region": "apac", "service": "catalog", "latency_ms": 160.74, "uptime_pct": 97.407, "timestamp": 20250302},
    # ... (include ALL your data here exactly as in your JSON file)
    {"region": "amer", "service": "support", "latency_ms": 198.86, "uptime_pct": 98.624, "timestamp": 20250312}
]

@app.post("/analyze")
async def analyze_latency(request: RequestData):
    results = {}
    
    for region in request.regions:
        region_data = [d for d in data if d["region"] == region]
        
        if not region_data:
            continue
            
        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        avg_uptime = np.mean(uptimes)
        breaches = sum(1 for latency in latencies if latency > request.threshold_ms)
        
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return results
