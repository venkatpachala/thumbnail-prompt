# thumbnail-generator

Locally runnable demo that generates YouTube thumbnails from a text prompt and uploaded photo. Frontend uses Next.js and backend uses FastAPI.

## Prerequisites
- Python 3.10+
- Node.js 18+
- Git

## Backend setup
```bash
python -m venv venv
# Windows: .\venv\Scripts\Activate
# Linux/Mac: source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

## Frontend setup
```bash
cd frontend
npm install
# create env
# echo NEXT_PUBLIC_API_URL=http://127.0.0.1:8000 > .env.local
npm run dev
```

Optional: set `HF_HOME` to a drive with space for model downloads.

## Troubleshooting
- onnxruntime missing → `pip install onnxruntime`
- CUDA OOM → use smaller resolutions; pipeline uses sequential CPU offload.
- Cannot download model → manually download from Hugging Face and set `HF_HOME`.
