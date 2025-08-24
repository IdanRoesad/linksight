from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from .services import get_ai_analysis
from pathlib import Path
from .config import settings 

current_dir = Path(__file__).parent
base_dir = current_dir.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()
origins = [
    "http://localhost:3000",
    "https://web.postman.co",
    "chrome-extension://gfgnmhcnajnlhoekjdechigdbgalklda"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/analyze")
async def options_analyze():
    return Response(status_code=200)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
auth_scheme = HTTPBearer(auto_error=False)
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    try:
        user_response = supabase.auth.get_user(token.credentials)
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.post("/analyze")
async def analyze_job(request: Request, current_user: dict = Depends(get_current_user)):
    request_data = await request.json()
    job_text = request_data.get("job_text")

    if not job_text:
        raise HTTPException(status_code=400, detail="job_text is required")

    ai_results = get_ai_analysis(job_text)
    if ai_results.get("error"):
        raise HTTPException(status_code=500, detail=ai_results["error"])

    new_analysis_data = {
        "user_id": current_user.id,
        "job_title": request_data.get("job_title"),
        "company_name": request_data.get("company_name"),
        "linkedin_url": request_data.get("linkedin_url"),
        "ai_summary": ai_results.get("summary"),
        "ai_requirements": ai_results.get("requirements"),
        "ai_action_plan": ai_results.get("action_plan")
    }

    try:
        data, count = supabase.table("job_analyses").insert(new_analysis_data).execute()
        return data[1][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")