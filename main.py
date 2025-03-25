from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from starlette.requests import Request

from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"],
                   )

# Mount the static directory to serve HTML, CSS, and JS files

app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates directory

templates = Jinja2Templates(directory="static")

# Include API routes from different modules

from routes import users, posts, comments

app.include_router(users.router)

app.include_router(posts.router)

app.include_router(comments.router)

# Home route to serve index.html

@app.get("/", response_class=HTMLResponse)

def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request}) 