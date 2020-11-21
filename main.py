import sys
import os
import pathlib

from os.path import join
from fastapi import FastAPI , HTTPException , Header , Depends
from routers import routers
from fastapi.middleware.cors import CORSMiddleware

from dependency.container import Container
from dependency_injector.wiring import inject , Provide


def get_content_type(content_type: str = Header("Content-Type")) -> None:

    """
     Check if content type is valid for each request
    """
    if content_type != "application/json":
        raise HTTPException(status_code=415, detail="Unsupported Media Type, must be application/json")

@inject
def create_app(container : Container , nano_node_router : routers.NanoNode = Provide[Container.router_nano]) -> FastAPI:
    app = FastAPI()
    app.container = container

    # Allow all origins to be able to use the front end 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials = True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(
        nano_node_router,
        tags=["node"],
        dependencies=[Depends(get_content_type)],
        responses={404: {"description": "Not found"}})
    
    return app


def create_container() -> Container:
    # Define dependency injections
    container = Container()
    container.config.from_yaml( join("resources" , "app.yml") ) # Get app configs from yaml
    container.log.init_resources()
    container.wire(modules=[sys.modules[__name__]])
    return container

def create_log_file() -> None:

    folder = join("logs")
    file_log = "output.log"
    if pathlib.Path(join(folder , file_log)).is_file(): # File already exists
        return    
    
    os.mkdir(folder)  # Python>3.2
    with open (join( folder , file_log) , "w") as file: # Create file
        pass

create_log_file()
container = create_container();
app       = create_app(container)
