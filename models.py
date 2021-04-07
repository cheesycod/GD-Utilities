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

class Promotion(Model):
    user = fields.ForeignKeyField('models.User', related_name='promotions')
    message_id = fields.BigIntField()
    channel_id = fields.BigIntField()
    category_id = fields.BigIntField()
    promo_id = fields.IntField()
    reply_id = fields.BigIntField()