from contextlib import asynccontextmanager
import quart.flask_patch
from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired
from quart import Quart, render_template, request, redirect, Blueprint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from src.backend.models import Game, GameDAL, GameForm

home_api = Blueprint("home_api", __name__)

# Initialize SQLAlchemy with a test database
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

@home_api.before_app_serving
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # This resets the database - remove for a real project!
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with game_dal() as bd:
            await bd.create_game("title", "description", "tools", "game_type")

@asynccontextmanager
async def game_dal():
    async with async_session() as session:
        async with session.begin():
            yield GameDAL(session)

@home_api.route("/api")
def hello_test():
    return("Hello World")


########################
## Database Endpoints ##
########################

@home_api.route("/api/stage_games")
async def get_stage_games():
    async with game_dal() as gd:
        return await gd.filter_games("stage")

@home_api.route("/api/warmup_games")
async def get_warmup_games():
    async with game_dal() as gd:
        return await gd.filter_games("warmup")

@home_api.route("/api/all_games")
async def get_all_games():
    async with game_dal() as gd:
        return await gd.get_all_games()

@home_api.route("/api/game/<string:game_id>")
async def get_game(game_id):
    async with game_dal() as gd:
        return await gd.get_game(f"{ game_id }")

@home_api.route("/api/create_game", methods=["GET", "POST"])
async def create_game():
    form = GameForm()
    if request.method == "POST":
        async with game_dal() as gd:
            await gd.create_game(form.title.data, form.description.data, form.tools.data, form.game_type.data)
        return redirect("/api/all_games")
    return await render_template("create_game.html", form=form)
