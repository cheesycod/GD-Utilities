config = 0 # 0 = main, 1 = test


if config == 0:
    token = "NzczODk1NjAyNzQ4MzkxNDY1.X6P4cQ.HLKn56cvI3QhGwCvfuCRYKU7Ge4"

    promo_category = [
    830420996241489951, # Partners
    830420997030412308, # Promote
    830420998343622677, # Social Media/Others
    830420992589430785  # Sponsors
    ]
    
    ignore_checks = [830420998343622677] # Categories to ignore checks
    
    db = "prod.sqlite3"
    
    ad_channel = 830421039640739850
    warn_channel = 830421040474882068
    mod_logs = 830421036607602688
    mute_role = 830421063078903870
    
    guild_id = 830067078815023124

elif config == 1:
    token = "NzM4ODMyMTYzOTUyMzk0Mjk2.XyRpEg.3vYSwgUQirM469xVRBQA1dTPUQ0"
    
    promo_category = [
    829402297603326042,
    829402297603326047,
    829402297926811655,
    829402298701709323
    ]
    
    ignore_checks = []
    
    db = "test.sqlite3"

    ad_channel = 829402296852938863
    warn_channel = 0
    mod_logs = 0
    mute_role = 0
    guild_id = 0

ad_rules = f"""
Please see <#{ad_channel}> for more information on how to advertise. Advertisements which do not follow these rules may be deleted and you may be punished if you break the rules too often. Thank you for using PB! Have a nice day!

"""

promo_min_len = 20