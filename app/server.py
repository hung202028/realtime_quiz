import threading
from contextlib import asynccontextmanager

import prometheus_client
import uvicorn
from fastapi import FastAPI

from app.models.dependency import container
from app.models.quiz.router import router as quiz_router


def start_prometheus(port: int):
    prometheus_client.start_http_server(port=port)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configs = container.get_configs()
    prometheus = threading.Thread(target=start_prometheus, args=(configs.PROMETHEUS_PORT,), daemon=True)
    prometheus.start()
    yield

    clients = container.get_clients()
    await clients.cache.close()
    for _, connections in container.get_socket_manager().active_connections.items():
        for websocket in connections:
            await websocket.close()


app = FastAPI(title="Quiz WebSocket Server", lifespan=lifespan)
app.include_router(quiz_router, prefix="/api/v1", tags=["API Endpoints"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
