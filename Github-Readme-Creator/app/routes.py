from fastapi import APIRouter, HTTPException
from app.models import RepoRequest, ReadmeResponse
from app.services import generate_readme_from_url
from pydantic import ValidationError

router = APIRouter()

@router.get("/")
async def health_check():
    return {"message": "OK"}

@router.post("/generate")
async def generate(request: RepoRequest):
    try:
        readme = await generate_readme_from_url(request.url, request.token)
        return {"readme": readme}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"message": "OK"}
