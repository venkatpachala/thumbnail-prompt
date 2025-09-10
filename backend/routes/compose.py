from __future__ import annotations

import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image

from ..utils import image_utils, paths

router = APIRouter(prefix="/compose", tags=["compose"])
logger = logging.getLogger(__name__)


class ComposeRequest(BaseModel):
    background_path: str
    cutout_path: str
    headline: str
    output_size: tuple[int, int] = (1280, 720)
    layout: str = "subject-right"


def _resolve(public_path: str, subdir: str) -> Path:
    name = Path(public_path).name
    return paths.file_path(subdir, name)


@router.post("/thumbnail")
async def compose_thumb(req: ComposeRequest):
    try:
        bg_path = _resolve(req.background_path, "backgrounds")
        cutout_path = _resolve(req.cutout_path, "cutouts")
        bg = Image.open(bg_path)
        cutout = Image.open(cutout_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image paths") from e

    logger.info("Composing thumbnail")
    bg = image_utils.fit_canvas(bg, req.output_size)
    side = "right" if req.layout == "subject-right" else "left"
    composed = image_utils.place_subject(bg, cutout, side)
    text_side = "left" if side == "right" else "right"
    composed = image_utils.add_headline(composed, req.headline, side=text_side)

    filename = paths.safe_filename("thumb", "png")
    file_path = paths.file_path("thumbnails", filename)
    composed.save(file_path)
    logger.info("Thumbnail saved to %s", file_path)
    return {"thumbnail_path": paths.public_url("thumbnails", filename)}
