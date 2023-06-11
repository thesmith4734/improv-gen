from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
import quart.flask_patch
from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired

# Initialize SQLAlchemy with a test database
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# Data Model
class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    tools = Column(String)
    game_type = Column(String)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tools": self.tools,
            "game_type": self.game_type
        }

# Data Access Layer
class GameDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_game(
        self,
        title,
        description,
        tools,
        game_type,
    ):
        new_game = Game(
            title = title,
            description = description,
            tools = tools,
            game_type = game_type,
        )
        self.db_session.add(new_game)
        await self.db_session.flush()
        return new_game.json()

    async def get_all_games(self):
        query_result = await self.db_session.execute(select(Game).order_by(Game.id))
        return [user.json() for user in query_result.scalars().all()]

    async def filter_games(self, select_game_type):
        query_result = await self.db_session.execute(select(Game).filter_by(game_type=select_game_type))
        return [user.json() for user in query_result.scalars().all()]

    async def get_game(self, game_id):
        query = select(Game).where(Game.id == game_id)
        query_result = await self.db_session.execute(query)
        user = query_result.one()
        return user[0].json()

# Form implementation for Games
class GameForm(FlaskForm):
    title = f.StringField("title", validators=[DataRequired()])
    description = f.StringField("description", validators=[DataRequired()])
    tools = f.StringField("tools")
    game_type = f.StringField("game_type")

    display = ["title", "description", "tools", "game_type"]