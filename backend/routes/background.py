from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image

from ..utils import sd_pipeline, paths

router = APIRouter(prefix="/background", tags=["background"])
logger = logging.getLogger(__name__)


class BgRequest(BaseModel):
    prompt: str
    width: int = 768
    height: int = 512


@router.post("/generate")
async def generate_bg(req: BgRequest):
    try:
        logger.info("Generating background: %s", req.prompt)
        img: Image.Image = sd_pipeline.txt2img(req.prompt, req.width, req.height)
    except Exception as e:
        logger.exception("SD generation failed")
        raise HTTPException(status_code=500, detail=str(e))

    filename = paths.safe_filename("bg", "png")
    file_path = paths.file_path("backgrounds", filename)
    img.save(file_path)
    logger.info("Background saved to %s", file_path)
    return {"background_path": paths.public_url("backgrounds", filename)}
