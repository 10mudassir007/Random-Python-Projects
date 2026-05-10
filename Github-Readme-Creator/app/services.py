import httpx
import asyncio
import base64
import json
from app.config import SKIP_DIRS, SKIP_EXTENSIONS, get_github_token, get_llm

def parse_url(url: str):
    parts = url.rstrip("/").split("/")
    return parts[-2], parts[-1]

async def fetch_all_files(api_url: str, token: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            api_url,
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()["tree"]

def build_structure(tree_items):
    structure = []
    for item in tree_items:
        if any(skip in item["path"] for skip in SKIP_DIRS):
            continue
        if any(item["path"].endswith(ext) for ext in SKIP_EXTENSIONS):
            continue
        prefix = "  " * (item["path"].count("/"))
        name = item["path"].split("/")[-1]
        structure.append(f"{prefix} {name}")
    return "\n".join(structure)

async def fetch_repo_metadata(owner: str, repo: str, token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        data = response.json()
        return {
            "description": data.get("description"),
            "language": data.get("language"),
            "topics": data.get("topics"),
        }

async def fetch_readme(owner: str, repo: str, token: str) -> str | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/readme",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return base64.b64decode(response.json()["content"]).decode("utf-8")

async def fetch_all_contents(tree_items: list, token: str) -> dict:
    async with httpx.AsyncClient() as client:
        filtered = [
            item for item in tree_items
            if item["type"] == "blob"
            and not any(skip in item["path"] for skip in SKIP_DIRS)
            and not any(item["path"].endswith(ext) for ext in SKIP_EXTENSIONS)
        ]
        tasks = [
            client.get(item["url"], headers={"Authorization": f"Bearer {token}"})
            for item in filtered
        ]
        responses = await asyncio.gather(*tasks)
        contents = {}
        for item, response in zip(filtered, responses):
            response.raise_for_status()
            contents[item["path"]] = base64.b64decode(response.json()["content"]).decode("utf-8")
        return contents

def extract_notebook_code(content: str) -> str:
    notebook = json.loads(content)
    code = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            code.append("".join(cell["source"]))
    return "\n\n".join(code)

def limit_lines(content: str, max_lines: int = 1000) -> str:
    return "\n".join(content.split("\n")[:max_lines])

def content_preprocessing(contents: dict) -> dict:
    contents = {
        name: extract_notebook_code(content) if name.endswith(".ipynb") else content
        for name, content in contents.items()
    }
    return {name: limit_lines(content) for name, content in contents.items()}

def structure_prompt(owner, repo, structure, metadata, readme, contents):
    prompt = "You are an assistant for writing GitHub README files. Analyze the details below and write a detailed GitHub README in markdown.\n\n"
    prompt += f"Owner: {owner}\n"
    prompt += f"Repo: {repo}\n\n"
    prompt += f"File/Folder Structure:\n{structure}\n\n"
    prompt += f"Metadata:\n{metadata}\n\n"
    if readme:
        prompt += f"Existing README:\n{readme}\n\n"
    total_words = sum(len(code.split()) for code in contents.values())
    if total_words < 5000:
        prompt += "File Contents:\n"
        for name, code in contents.items():
            prompt += f"\n### {name}\n{code}\n"
    else:
        prompt += "File Contents (truncated):\n"
        for name, code in contents.items():
            truncated = " ".join(code.split()[:200])
            prompt += f"\n### {name}\n{truncated}\n"
    return prompt

async def generate_readme_from_url(url: str, token: str | None = None) -> str:
    token = token or get_github_token()
    owner, repo = parse_url(url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    
    files = await fetch_all_files(api_url, token)
    structure = build_structure(files)
    metadata = await fetch_repo_metadata(owner, repo, token)
    readme = await fetch_readme(owner, repo, token)
    contents = await fetch_all_contents(files, token)
    contents = content_preprocessing(contents)
    prompt = structure_prompt(owner, repo, structure, metadata, readme, contents)

    llm = get_llm()
    result = llm.invoke([("human", prompt)])
    return result.content[0]["text"]