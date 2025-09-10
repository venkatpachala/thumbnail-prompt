from __future__ import annotations

import logging
from typing import Optional

import torch
from diffusers import StableDiffusionPipeline

_PIPELINE: Optional[StableDiffusionPipeline] = None


logger = logging.getLogger(__name__)


def get_sd_pipeline() -> StableDiffusionPipeline:
    global _PIPELINE
    if _PIPELINE is not None:
        return _PIPELINE

    model_id = "runwayml/stable-diffusion-v1-5"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("Loading Stable Diffusion pipeline on %s", device)
    dtype = torch.float16 if device == "cuda" else torch.float32
    _PIPELINE = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=dtype, safety_checker=None
    )
    if device == "cuda":
        _PIPELINE.to(device)
        _PIPELINE.enable_attention_slicing()
        _PIPELINE.enable_sequential_cpu_offload()
    else:
        logger.warning("CUDA not available, using CPU – generation will be slow")
    return _PIPELINE


def txt2img(prompt: str, width: int = 768, height: int = 512):
    pipe = get_sd_pipeline()
    generator = torch.Generator(device=pipe.device).manual_seed(42)
    image = pipe(prompt, width=width, height=height, guidance_scale=7.5, generator=generator).images[0]
    return image
