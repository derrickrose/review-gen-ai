from fastapi import FastAPI
import uvicorn
from helpers import find_steps

import steps.step0_setup

import logging
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/") == -1

# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

app = FastAPI(docs_url="/")

for module, module_name in find_steps():
    if hasattr(module, 'router'):
        app.include_router(module.router, tags=[module_name])

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
