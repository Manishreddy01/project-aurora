from fastapi import FastAPI
from routes.upload import router as uploadRouter
from routes.query import router as queryRouter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# CORS setup — update this with actual frontend URL if known
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
    # Add deployed domain here later (e.g. "https://mychatbot.com")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict to ["POST"] if needed
    allow_headers=["*"],
)

app.include_router(uploadRouter, prefix="/upload")
app.include_router(queryRouter, prefix="/query")

@app.get("/health")
async def health_check():
    return { "status": "ok" }
