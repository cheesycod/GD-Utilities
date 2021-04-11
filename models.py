from tortoise.models import Model
from tortoise import fields


class User(Model):
    """Represents a user"""
    id = fields.BigIntField(pk=True)
    level = fields.IntField()

    def __str__(self):
        return str(self.id)

class Warning(Model):
    user = fields.ForeignKeyField('models.User', related_name='warns')
    case = fields.IntField()
    reason = fields.TextField()
    severity = fields.IntField()
    mod = fields.BigIntField()

class Promotion(Model):
    user = fields.ForeignKeyField('models.User', related_name='promotions')
    message_id = fields.BigIntField()
    channel_id = fields.BigIntField()
    category_id = fields.BigIntField()
    promo_id = fields.IntField()
    reply_id = fields.BigIntField()
    
class Reaction(Model):
    channel_id = fields.BigIntField()
    message_id = fields.BigIntField()
    role_id = fields.BigIntField()
    emoji_id = fields.BigIntField()

class Mute(Model):
    automod = fields.BooleanField(default = False)
    seconds = fields.BigIntField(null = True)
    user = fields.ForeignKeyField('models.User', related_name='mutes')
    reason = fields.TextField()
    start_time = fields.BigIntField()
    handled = fields.BooleanField()

class Tag(Model):
    name = fields.TextField()
    content = fields.TextField()