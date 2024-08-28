import os

from pydbantic import Database

from models import ChannelData

db_path = "data"
db_filename = "prod.db"


async def create_db():
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    db = await Database.create(
        f"sqlite:///{os.path.join(db_path, db_filename)}",
        tables=[
            ChannelData,
        ],
    )
