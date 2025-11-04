"""
VENOM API Server
Provides both FastAPI REST endpoints and gRPC services
"""

import logging
import asyncio
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import fractal functions
from .fractal import time_wrap, fractal_total, mobius_time, grav_mode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VENOM Λ-Genesis API",
    description="Time compression and fractal computation services",
    version="1.0.0"
)


# Request/Response models
class TimeWrapRequest(BaseModel):
    k: float = 1.5
    p: float = 0.75
    u: float = 0.2
    t1: float = 1000.0


class FractalTotalRequest(BaseModel):
    s: float = 5.0
    theta: float = 0.7


class MobiusTimeRequest(BaseModel):
    s: float = 1000.0
    k: float = 1.5
    p: float = 0.75
    u: float = 0.2
    theta: float = 0.7


class GravModeRequest(BaseModel):
    s: float = 1000.0
    theta: float = 0.7
    k: float = 1.5
    p: float = 0.75
    u: float = 0.2


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "VENOM Λ-Genesis API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "venom-api"}


@app.post("/time_wrap")
async def api_time_wrap(request: TimeWrapRequest):
    """Time wrap endpoint"""
    try:
        result = time_wrap(request.k, request.p, request.u, request.t1)
        return {
            "wrapped_time": result,
            "original": request.t1,
            "compression_ratio": request.t1 / result if result > 0 else 0
        }
    except Exception as e:
        logger.error(f"Error in time_wrap: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fractal_total")
async def api_fractal_total(request: FractalTotalRequest):
    """Fractal total speedup endpoint"""
    try:
        result = fractal_total(request.s, request.theta)
        return {
            "total_speedup": result,
            "sequential": request.s,
            "theta": request.theta
        }
    except Exception as e:
        logger.error(f"Error in fractal_total: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mobius_time")
async def api_mobius_time(request: MobiusTimeRequest):
    """Möbius time compression endpoint"""
    try:
        result = mobius_time(request.s, request.k, request.p, request.u, request.theta)
        return {
            "compressed_time": result,
            "original": request.s,
            "compression_factor": request.s / result if result > 0 else 0
        }
    except Exception as e:
        logger.error(f"Error in mobius_time: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/grav_mode")
async def api_grav_mode(request: GravModeRequest):
    """Gravitational mode endpoint"""
    try:
        result = grav_mode(request.s, request.theta, request.k, request.p, request.u)
        return result
    except Exception as e:
        logger.error(f"Error in grav_mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Main entry point"""
    logger.info("Starting VENOM API server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
