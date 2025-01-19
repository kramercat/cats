from database.base_model import BaseModel
import utils.datetime_utils as datetime_utils


class Guilds(BaseModel):
    class Meta:
        table = "guilds"
        columns = {
            "guild_id": "TEXT",
            "guild_name": "TEXT",
            "join_date": "DATETIME",
            "leave_date": "DATETIME",
        }

    @classmethod
    def insert_guild(cls, guild_id: int, guild_name: str):
        """Insert a new guild into the guilds table."""
        join_date = datetime_utils.now()
        values = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "join_date": join_date,
            "leave_date": None,
        }
        cls.create(values)

    @classmethod
    def update_guild_leave_date(cls, guild_id: int):
        """Update the leave date for a guild."""
        set_values = {"leave_date": datetime_utils.now()}
        where_values = {"guild_id": guild_id}
        cls.update(set_values, where_values)
