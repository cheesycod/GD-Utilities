from discord.ext.commands import Cog, command, has_guild_permissions, bot_has_guild_permissions
from discord import Role, Member, User, Embed, Color
import models
from config import promo_category, ad_rules, promo_min_len

async def get_user_obj(id, related = None):
    if related:
        user_obj = await models.User.filter(id=id).prefetch_related(related)
    else:
        user_obj = await models.User.filter(id=id)
    if user_obj == []:
        user_obj = models.User(id = id, level = 0)
        await user_obj.save()
        return await get_user_obj(id, related)
    return user_obj[0]