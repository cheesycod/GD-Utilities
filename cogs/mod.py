from deps import *

class Mod(Cog):
    def __init__(self, client):
        self.client = client
    
    async def role_check(self, ctx, mod, target, type):
        if target.top_role.position >= mod.top_role.position:
            await ctx.send(f"You cannot {type} people who are below or at the same level as you in role hierarchy")
            return False
        else:
            return True
    
    @command(pass_context = True)
    @has_guild_permissions(kick_members = True)
    @bot_has_guild_permissions(kick_members = True)
    async def kick(self, ctx, member: Member, *, reason: str = "There was no reason specified"):
        if (await self.role_check(ctx, ctx.author, member, "kick")) == False:
            return

        try:
            await member.send(f"You have been kicked from this server for reason: {reason}")
        except:
            pass
        await member.kick(reason = reason)
        await ctx.send("Member was kicked :)")

    @command(pass_context = True)
    @has_guild_permissions(ban_members = True)
    @bot_has_guild_permissions(ban_members = True)
    async def ban(self, ctx, member: Member, *, reason: str = "There was no reason specified"):
        if (await self.role_check(ctx, ctx.author, member, "ban")) == False:
            return
        try:
            await member.send(f"You have been banned from this server for reason: {reason}")
        except:
            pass
        await member.ban(reason = reason)
        await ctx.send("Member was banned :)")
    
    @command(pass_context = True)
    @has_guild_permissions(ban_members = True)
    @bot_has_guild_permissions(ban_members = True)
    async def unban(self, ctx, user: User):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} has been unbanned")
    
    @command(pass_context = True)
    @has_guild_permissions(manage_messages = True)
    @bot_has_guild_permissions(manage_messages = True)  
    async def warn(self, ctx, user: User, reason: str):
        user_obj = await get_user_obj(user.id, related = "warns")
        print(user_obj)
        warn = models.Warning(case = len(user_obj.warns) + 1, reason = reason, severity = 1, user = user_obj)
        print(user_obj.warns.all())
        await user_obj.save()
        await warn.save()
        await user.send(f"You have been warned in this server for the reason: {reason}")
        await ctx.send(f"User has been warned and now has {len(user_obj.warns)} warnings!")
    
    @command(pass_context = True)
    async def catid(self, ctx):
        """Returns the category ID"""
        if ctx.channel.category:
            return await ctx.send(str(ctx.channel.category.id))
        return await ctx.send("No category attached to this channel")
    
def setup(client):
    client.add_cog(Mod(client))