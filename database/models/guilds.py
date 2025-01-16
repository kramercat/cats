import utils.datetime_utils as datetime_utils
from database.base_model import BaseModel

from datetime import datetime
from zoneinfo import ZoneInfo


class Guilds(BaseModel):
    table = "guilds"
    columns = ["guild_id", "guild_name", "join_date", "leave_date"]

    @classmethod
    def insert_guild(cls, db_manager, guild_id: int, guild_name: str):
        """Insert a new guild into the guilds table."""
        join_date = datetime_utils.now()
        values = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "join_date": join_date,
            "leave_date": None,
        }
        cls.create(db_manager, values)

    @classmethod
    def update_guild_leave_date(cls, db_manager, guild_id: int):
        """Update the leave date for a guild."""
        set_values = {"leave_date": datetime_utils.now()}
        where_values = {"guild_id": guild_id}
        cls.update(db_manager, set_values, where_values)
