config = 1 # 0 = main, 1 = test


if config == 0:
    token = "NzczODk1NjAyNzQ4MzkxNDY1.X6P4cQ.HLKn56cvI3QhGwCvfuCRYKU7Ge4"

    promo_category = [
    828302398753734659, # Special Advertising
    828303365796134943, # Other Advertisements
    828303395394813952, # Advertisements
    828332585598844968 # Other Ads
    ]
    
    db = "prod.sqlite3"

elif config == 1:
    token = "NzM4ODMyMTYzOTUyMzk0Mjk2.XyRpEg.3vYSwgUQirM469xVRBQA1dTPUQ0"
    
    promo_category = [
    829402297603326042,
    829402297603326047,
    829402297926811655,
    829402298701709323
    ]
    
    db = "test.sqlite3"

ad_rules = """
__**- Advertising #Rules IMPORTANT!!**__

The Path of Warnings (depends on situation)

♦️ `1` Warning = Warning OR mute 4 Hours
♦️ `2` Warning = Warning OR mute 8 Hours
♦️ `3` Warning = 2 Days mute from the server
♦️ `4` Warning = Server Ban.

🔹 Duplicate advertisements are not allowed in same section
🔹 All advertisements must be posted in the correct channel
🔹 You must wait 2 Hours before reposting a posted advertisement
🔹 Only post your advertisement in correct Sections/Logs/Channels
🔹 Your advertisement must include a description and a discord.gg link OR Post in <#828315007187681280>
🔹 Your advertisement should not contain any malicious links/script/program/hacking/toxic etc.
🔹 The servers advertisement should follow Discord TOS!
🔹 Pay pal servers are not allowed!
🔹 DM Advertising will result instant Ban + Report <#828316458730913792> 
🔹 ONLY English Text Advertisements!
🔹 NSFW content or servers are not allowed outside of <#828315109469454366> 
🔹 The use of nudity banners in <#828315109469454366> -servers should be minor nudity 
🔹 Your advertisement will be deleted if you leave the server!
🔹 No expired discord invites links = DELETE(kick/ban depends on situation)

Advertisements will be deleted
🔸 A description wasn’t provided or description is full of useless characters to pass our characters limit
🔸 Invite is expired
🔸 Contains malicious links/script/program (The author of the post will be instant ban from this server)
🔸 Contains about selling accounts, distribution/selling of hacks, join to gain money (Can result in a ban/mute/kick)
🔸 The author left this server

__**NOTE**__

🔸 Moderators reserve the right to delete your advertisement without any notice
🔸 Moderators reserve the right to restrict you from the advertisement channels with any given duration
🔸 Moderators decisions are final!
"""

promo_min_len = 20