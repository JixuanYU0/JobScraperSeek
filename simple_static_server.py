"""Simple test server to verify static file serving works."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path("static")
index_file = static_dir / "index.html"

# Mount assets
if (static_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")

# API route first
@app.get("/api/test")
async def test():
    return {"message": "API works"}

# Frontend routes
if index_file.exists():
    @app.get("/", response_class=HTMLResponse)
    async def root():
        return index_file.read_text()

    @app.get("/vite.svg")
    async def vite_svg():
        svg_file = static_dir / "vite.svg"
        if svg_file.exists():
            return FileResponse(svg_file)
        return {"error": "not found"}

    @app.get("/{catchall:path}", response_class=HTMLResponse)
    async def catchall(catchall: str):
        if catchall.startswith("api"):
            return {"error": "API not found"}
        return index_file.read_text()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
