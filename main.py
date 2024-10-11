from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from your_markov_chain_file import MarkovChainStoryGenerator
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from pathlib import Path

app = FastAPI()

# Serve static files (e.g., CSS) and HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow CORS for frontend (adjust `allow_origins` based on your actual frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize story generator
unsplash_access_key = "YOUR_UNSPLASH_ACCESS_KEY"
story_generator = MarkovChainStoryGenerator(unsplash_access_key)

class StoryRequest(BaseModel):
    characters: list
    plot: str
    age_range: str
    genre: str
    max_length: int

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_file = Path("templates/index.html").read_text()
    return HTMLResponse(content=html_file, status_code=200)

@app.post("/generate-story")
async def generate_story(request: StoryRequest):
    # Generate the story
    story = story_generator.generate(
        characters=request.characters,
        plot=request.plot,
        age_range=request.age_range,
        genre=request.genre,
        max_length=request.max_length
    )
    
    # Fetch images for characters
    images = []
    for character in request.characters:
        image_urls = story_generator.fetch_images(character.strip())
        images.extend(image_urls)
    
    return {
        "story": story,
        "images": images
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
