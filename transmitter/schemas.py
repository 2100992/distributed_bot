from marshmallow import fields, Schema


FromSchema = Schema.from_dict(
    {
        'id': fields.Int(),
        'is_bot': fields.Bool(),
        'first_name': fields.Str(),
        'last_name': fields.Str(),
        'username': fields.Str(),
        'language_code': fields.Str()
    }
)

ChatSchema = Schema.from_dict(
    {
        'id': fields.Int(),
        'title': fields.Str(),
        'first_name': fields.Str(),
        'last_name': fields.Str(),
        'username': fields.Str(),
        'type': fields.Str(),
        'all_members_are_administrators': fields.Bool()
    }
)

EntitiesSchema = Schema.from_dict(
    {
        'offset': fields.Int(),
        'length': fields.Int(),
        'type': fields.Str()
    }
)

MessageSchema = Schema.from_dict(
    {
        'message_id': fields.Int(),
        'from': fields.Nested(FromSchema),
        'chat': fields.Nested(ChatSchema),
        'date': fields.Int(),
        'text': fields.Str(),
        'entities': fields.Nested(EntitiesSchema, many=True)
    }
)

RabbitReplySchema = Schema.from_dict(
    {
        'message': fields.Nested(MessageSchema),
        'text': fields.Str()
    }
)
