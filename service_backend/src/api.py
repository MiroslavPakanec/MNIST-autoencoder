import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from static.render import render
from src.utilities.environment import Environment
from src.utilities.logging.config import (initialize_logging, initialize_logging_middleware)
from src.utilities.utilities import get_uptime
from src.routers.sampling_router import sampling_router
from src.routers.model_router import model_router
from src.routers.watermark_router import watermark_router

app = FastAPI()

initialize_logging()
initialize_logging_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(watermark_router, tags=['Watermarks'])
app.include_router(sampling_router, tags=['Sampling'])
app.include_router(model_router, tags=['Model'])

@app.get('/health')
def health():
    return {
        "service": Environment().COMPOSE_PROJECT_NAME,
        "uptime": get_uptime()
    }

@app.get('/')
def index():
    return HTMLResponse(
        render(
            'static/index.html',
            host=Environment().HOST_IP,
            port=Environment().API_CONTAINER_PORT
        )
    )

if __name__ == '__main__':

    uvicorn.run(
        'api:app',
        host=Environment().HOST_IP,
        port=Environment().API_CONTAINER_PORT
    )
