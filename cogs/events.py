from deps import *

class Events(Cog):
    def __init__(self, client):
        self.client = client
        self.handle_mutes.start()
    
    async def _record_promotion(self, message, reply_id):
        user_obj = await get_user_obj(message.author.id, related = "promotions")
        promotion = models.Promotion(message_id = message.id, channel_id = message.channel.id, category_id = message.channel.category.id, promo_id = len(user_obj.promotions) + 1, reply_id = reply_id, user = user_obj)
        await user_obj.save()
        await promotion.save()
    
    @Cog.listener()
    async def on_message(self, message):
        # Ignore bots and dms
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        # Handle promotion stuff
        if message.channel.category is None or message.channel.category.id not in promo_category:
            pass
        else:
            valid = True
            if "no-desc" in str(message.channel) or message.channel.category.id in ignore_checks:
                pass
            elif len(message.content) < promo_min_len:
                valid = False
            
            elif "discord.gg/" in message.content or "discord.com/" in message.content:
                pass
            else:
                if valid:
                    valid = False

            if valid:
                # Valid promotion, send message
                embed = Embed(text = "Hi There!", color = Color.green(), description = f"**Welcome to PB!**\nPlease remember to follow our advertising rules\n**Our Rules**\n{ad_rules}")
                reply = await message.channel.send(embed = embed)
                
                # Record the promotion
                await self._record_promotion(message, reply.id)
                
            elif not valid:
                # Invalid, delete it
                await message.delete()
    
    @Cog.listener()
    async def on_member_join(self, member):
        print("Joined server")
        
        # Check for mute evasion
        user_obj = await get_user_obj(member.id, related = "mutes")
        async for mute in user_obj.mutes:
            if mute.handled:
                continue # Handled mute
            # Unhandled mute means mute evasion
            mute = member.guild.get_role(mute_role)
            await member.add_roles(mute, reason = "Mute Evasion Detection. Remuting")
            break
                
    @Cog.listener()
    async def on_member_remove(self, member):
        print("Left server")
        user_obj = await get_user_obj(member.id, related = "promotions")
        async for promotion in user_obj.promotions:
            channel = self.client.get_channel(promotion.channel_id)
            if channel is None:
                continue
            
            # Try to get and remove main message
            try:
                msg = await channel.fetch_message(promotion.message_id)
            except:
                msg = None
            print(channel, msg)
            if msg is not None:
                await msg.delete()
            
            # Try to get and remove reply as well
            try:
                msg = await channel.fetch_message(promotion.reply_id)
            except:
                msg = None
            if msg is not None:
                await msg.delete()
            
            await promotion.delete()

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        return await self._react_role_event(payload)
    
    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        return await self._react_role_event(payload)
        
    async def _react_role_event(self, payload):
        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member:
            pass
        elif payload.member:
            member = payload.member
        else:
            return
        
        if member.bot:
            return
        
        print(payload.emoji.id)
        reaction = await models.Reaction.filter(emoji_id = payload.emoji.id, message_id = payload.message_id, channel_id = payload.channel_id)
        
        # Always take the zeroth element
        if len(reaction) == 0:
            return
    
        reaction = reaction[0]
        
        role = guild.get_role(reaction.role_id)
        if role:
            if payload.event_type == "REACTION_ADD":
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

    @tasks.loop(seconds=10.0)
    async def handle_mutes(self):
        try: # Prevent people from breaking mute
            if not self.client.user:
                # Defer until on_ready is fired
                return
            # Fire mute event
            print("Mute handling triggered")
            mutes = await models.Mute.filter(handled = False).prefetch_related("user")
            print(mutes)
            for mute in mutes:
                if mute.handled or mute.seconds is None or time_mod.time() - mute.start_time < mute.seconds:
                    continue # Ignore handled mute, unlimited mutes and mutes that havent finished yet
                print(f"Handling mute {mute}")
                # Just taking off the roles should be enough. Autoresponder should handle the rest
                guild = self.client.get_guild(guild_id)
                mute_role_obj= guild.get_role(mute_role)
                user = guild.get_member(mute.user.id)
                await user.remove_roles(mute_role_obj, reason = f"Unmute due to mute expiry")
                
        except Exception as exc:
            print(exc)
        


def setup(client):
    client.add_cog(Events(client))