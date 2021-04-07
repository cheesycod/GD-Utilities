from deps import *

class Events(Cog):
    def __init__(self, client):
        self.client = client
    
    async def record_promotion(self, message, reply_id):
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

            if "no-desc" in str(message.channel):
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
                embed = Embed(text = "Hi There!", color = Color.green(), description = f"**Welcome to GP!**\nPlease remember to follow our advertising rules\n**Our Rules**\n{ad_rules}")
                reply = await message.channel.send(embed = embed)
                
                # Record the promotion
                await self.record_promotion(message, reply.id)
                
            elif not valid:
                # Invalid, delete it
                await message.delete()
                
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

def setup(client):
    client.add_cog(Events(client))