from contextlib import asynccontextmanager
from quart import Quart
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from os import urandom

from src.backend.api import home_api
from src.backend.models import GameDAL

# Create App
app = Quart(__name__)
app.register_blueprint(home_api)

# Set up CSRF
SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

def run() -> None:
    app.run()