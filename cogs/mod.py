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
    async def warn(self, ctx, user: Member, *, reason: str):
        """
        Gives a warning to a member. Needs the Manage Messages permission
        """
        user_obj = await get_user_obj(user.id, related = "warns")
        print(user_obj)
        warn = models.Warning(case = len(user_obj.warns) + 1, reason = reason, severity = 1, user = user_obj, mod = ctx.author.id)
        print(user_obj.warns.all())
        await user_obj.save()
        await warn.save()
        try:
            await user.send(f"You have been warned in this server for the reason: {reason}")
        except:
            pass
        await ctx.send(f"User has been warned and now has {len(user_obj.warns) + 1} warnings!")
        channel = self.client.get_channel(warn_channel)
        if channel is not None:
            await channel.send(f"{user.mention} has been warned for the reason: {reason}\n\nModerator: {ctx.author}")
    
    @command(pass_context = True)
    @has_guild_permissions(manage_messages = True)
    async def warnlog(self, ctx, user: Member):
        """
        Gets all warnings given to a member. Needs the Manage Messages permission
        """
        user_obj = await get_user_obj(user.id, related = "warns")
        print(user_obj)
        if len(user_obj.warns) == 0:
            return await ctx.send(f"{user} has no warnings")
        warnstr= ""
        i = 1
        async for warn in user_obj.warns:
            warnstr += f"**Warning {i}**\nReason: {warn.reason}\nModerator: <@{warn.mod}>\nWarn ID: {warn.id}\n\n"
            i+=1
        await ctx.send(warnstr)
        
    @command(pass_context = True)
    @has_guild_permissions(manage_messages = True)
    async def delwarn(self, ctx, warn_id: int):
        """
        Deletes a warning from a user given a warning id. Use warnlog to get this. Needs the Manage Messages permission
        """
        try:
            warn_id = int(warn_id)
        except:
            return await ctx.send("Warn ID must be a int")
        warn = await models.Warning.filter(id = warn_id).prefetch_related("user")
        if len(warn) == 0:
            return await ctx.send("Warning with provided Warn ID does not exist!")
        warn = warn[0]
        print(warn)
        await ctx.send(f"**<@{warn.user.id}> had one warning removed!**")
        await warn.delete()

    @command(pass_context = True)
    @has_guild_permissions(kick_members = True)
    async def clearwarn(self, ctx, user: Member):
        """
        Clear all warnings of a user. Needs the Kick Member permission
        """
        user_obj = await get_user_obj(user.id, related = "warns")
        print(user_obj)
        if len(user_obj.warns) == 0:
            return await ctx.send(f"{user} has no warnings to remove")
        i = 0
        async for warn in user_obj.warns:
            await warn.delete()
            i+=1
        return await ctx.send(f"Deleted {i} warnings!")
    
    @command(pass_context = True)
    @has_guild_permissions(manage_roles = True)
    async def reactrole(self, ctx, message: Message, role: Role, emoji: PartialEmoji):
        reactions = await models.Reaction.filter(emoji_id = emoji.id, message_id = message.id, channel_id = message.channel.id)
        if len(reactions) != 0:
            return await ctx.send("Reaction role already exists. Use delreactrole to remove it.")
        react_role = models.Reaction(channel_id = message.channel.id, message_id = message.id, role_id = role.id, emoji_id = emoji.id)
        await react_role.save()
        await message.add_reaction(emoji)
        await ctx.send("Setup reaction for this message successfully")
    
    @command(pass_context = True)
    @has_guild_permissions(manage_roles = True)
    async def delreactrole(self, ctx, message: Message, emoji: PartialEmoji = None):
        if emoji is None:
            emoji_kw = {}
        else:
            emoji_kw = {"emoji_id": emoji.id}
        reactions = await models.Reaction.filter(**emoji_kw, message_id = message.id, channel_id = message.channel.id)
        i = 0
        for reaction in reactions:
            try:
                channel = ctx.guild.get_channel(reaction.channel_id)
                msg = await channel.fetch_message(reaction.message_id)
                await msg.clear_reaction(emoji)
            except:
                pass
            await reaction.delete()
            i+=1
        return await ctx.send(f"Removed {i} reaction roles for this message")

    @command(pass_context = True)
    @has_guild_permissions(manage_messages = True)
    async def mute(self, ctx, user: Member, time: str, *, reason = "There was no reason specified"):
        """Mutes a member. Use 'u' as time for permamute"""
        time = self._parse_time(time)
        if type(time) == str:
            return await ctx.send(time)
        user_obj = await get_user_obj(user.id, related = "mutes")

        # Give member the muted role
        mute = ctx.guild.get_role(mute_role)
        await user.add_roles(mute, reason = f"Mute with reason: {reason}")

        # Add mute to database
        mute = models.Mute(seconds = time, start_time = int(time_mod.time()), user = user_obj, reason = reason, handled = False)
        await mute.save()
        await user_obj.save()
        return await ctx.send(f"Successfully muted {user.mention} for reason: {reason}")
        
    @command(pass_context = True)
    @has_guild_permissions(manage_messages = True)
    async def unmute(self, ctx, user: Member, reason: str = "There was no reason specified"):
        # Let autoresponder deal with updating database and dealing with that, our job is to just take off the role
        
        # Give member the muted role
        mute = ctx.guild.get_role(mute_role)
        await user.remove_roles(mute, reason = f"Unute with reason: {reason}")
        return await ctx.send(f"Successfully unmuted {user.mention} for reason: {reason}")

            
    def _parse_time(self, time):
        if time.replace(" ", "") == "u":
            return None
        modifier_string_sep = ", ".join(modifier_dict.keys())
        if type(time) != str:
            return "Time must be a string like 1d etc"
        proper_time = time[0:-1]
        try:
            proper_time = int(proper_time)
        except:
            return f"Could not get time. Make sure it is a proper integer followed by {modifier_string_sep}"
        mod = time[-1]
        try:
            mod = int(mod)
            return f"Your time does not have a modifier of {modifier_string_sep}"
        except:
            pass
        multiplier = modifier_dict.get(mod)
        if multiplier is None:
            return f"Your time does not have a modifier of {modifier_string_sep} because of reason: Invalid modifier '{mod}'"
        return multiplier*proper_time
        
def setup(client):
    client.add_cog(Mod(client))