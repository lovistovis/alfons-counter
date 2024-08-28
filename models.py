from typing import Dict, Optional

from pydantic import BaseModel
from pydbantic import DataBaseModel, PrimaryKey


class Counts(BaseModel):
    counts: Dict[int, float] = {}


class ChannelData(DataBaseModel):
    id: int = PrimaryKey()
    counts: Counts = Counts()

    @staticmethod
    async def fetch(id: int) -> Optional["ChannelData"]:
        return await ChannelData.get(id=id)
