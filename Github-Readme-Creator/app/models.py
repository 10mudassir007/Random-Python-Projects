from pydantic import BaseModel

class RepoRequest(BaseModel):
    url: str
    token: str | None = None

class ReadmeResponse(BaseModel):
    readme: str