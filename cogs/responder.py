from deps import *

class Responder(Cog):
    """Responds to events, logs them and possibly takes other actions against members"""
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_member_ban(self, guild, user):
       return await self._action_log(guild, user, "ban")

    @Cog.listener()
    async def on_member_unban(self, guild, user):
       return await self._action_log(guild, user, "unban")

    @Cog.listener()
    async def on_member_update(self, before, after):
        # Roles

        added_roles = [role for role in after.roles if role not in before.roles]
        
        removed_roles = [role for role in before.roles if role not in after.roles]
        
        print(added_roles, removed_roles)
        
        if added_roles or removed_roles:
            role_del_lst = [role.id for role in removed_roles] # For mute
            
            add_role_data = ", ".join([role.name for role in added_roles])
            
            # Get added role data otherwise default argument
            add_role_data = add_role_data if add_role_data else "No roles given"
            
            removed_role_data = ",".join([role.name for role in removed_roles])
            
            # Same with removed
            removed_role_data = removed_role_data if removed_role_data else "No roles removed"
            
            await self._action_log(after.guild, after, "role_update", extra_info = f"**Added Roles:** {add_role_data}\n**Removed Roles:** {removed_role_data}")
           
            # Handle the muted role being removed by setting handled to true
            role_del_lst = [role.id for role in removed_roles]
            if mute_role in role_del_lst:
                user_obj = await get_user_obj(after.id, related = "mutes")
                
                # Change all mutes to handled since manually unmuted
                async for mute in user_obj.mutes:
                    if mute.handled:
                        continue
                    print(f"Handling mute {mute}")
                    mute.handled = True
                    await mute.save()
                    await user_obj.save()

            # Make new mute object (permamute) for user if they are muted to ensure leaving before the mute is done causes mute to stick. These should be handled automatically
            role_add_lst = [role.id for role in added_roles]
            if mute_role in role_add_lst:
                user_obj = await get_user_obj(after.id, related = "mutes")
                mute = models.Mute(seconds = None, start_time = int(time_mod.time()), user = user_obj, reason = "Autoresponder flagged this user as they got the muted role", handled = False, automod = True)
                await mute.save()
                await user_obj.save()


    async def _action_log(self, guild, user, t, **kwargs):
        
        if t == "ban":
            title = "Member Banned"
            action = "been banned"
            check = AuditLogAction.ban
            color = Color.red()
        elif t == "unban":
            title = "Member Unbanned"
            action = "been unbanned"
            check = AuditLogAction.unban
            color = Color.red()
        elif t == "role_update":
            title = "Member Roles Updated"
            action = "had their roles updated"
            check = AuditLogAction.member_role_update
            color = Color.orange()

        if kwargs.get("reason") is None:
            async for entry in guild.audit_logs(action=check, limit = 1):
                reason = entry.reason if entry.reason is not None else "There was no reason specified/We could not get a reason"
                mod = entry.user
        else:       
            reason = kwargs["reason"]
        log_channel = guild.get_channel(mod_logs)

        extra_info = kwargs.get("extra_info") if kwargs.get("extra_info") is not None else "There is no extra information available for this action"

        embed = Embed(title = title, description = f"{user.mention} ({user}) has {action} on the server due to the actions of {mod.mention} ({mod}).\n**Created At**: {user.created_at}\n\n**Reason:** {reason}\n\n**Extra Information**\n\n{extra_info}", color = color)
        await log_channel.send(embed = embed)


def setup(client):
    client.add_cog(Responder(client))