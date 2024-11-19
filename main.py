from pathlib import Path

import uvicorn

from core.registrar import register_app

app = register_app()


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


if __name__ == '__main__':

    try:
        config = uvicorn.Config(app=f'{Path(__file__).stem}:app', reload=True)
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
