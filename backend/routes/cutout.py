from __future__ import annotations

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from rembg import remove
from PIL import Image
import io

from ..utils import paths

router = APIRouter(prefix="/cutout", tags=["cutout"])
logger = logging.getLogger(__name__)


@router.post("/remove")
async def remove_bg(image: UploadFile = File(...)):
    if image.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Invalid image type")
    data = await image.read()
    try:
        logger.info("Removing background from upload %s", image.filename)
        output = remove(data)
    except Exception as e:
        logger.exception("Background removal failed")
        raise HTTPException(status_code=500, detail=str(e))

    img = Image.open(io.BytesIO(output)).convert("RGBA")
    filename = paths.safe_filename("cutout", "png")
    file_path = paths.file_path("cutouts", filename)
    img.save(file_path)
    logger.info("Cutout saved to %s", file_path)
    return {"cutout_path": paths.public_url("cutouts", filename)}
