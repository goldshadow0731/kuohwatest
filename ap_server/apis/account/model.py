from flask.globals import request
from flask_restplus import Namespace, Resource, fields, model
from flask_restplus.inputs import _expand_datetime

api = Namespace("account", description=u"帳號及權限管理")


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})

login_input_payload = api.model(u'login帳號input', {
    'user_email': fields.String(required=True, example="itri@kuohwa.com"),
    'user_passwd': fields.String(required=True, example="tami")
})

login_output_payload = api.clone(u'login帳號output', base_input_payload)

forget_input_payload = api.model(u'forget帳號input', {
    'user_account': fields.String(required=True, example="tami")
})

forget_output_payload = api.clone(u'forget帳號output', base_input_payload)

add_account_input_payload = api.model(u'add帳號input', {
    'user_account': fields.String(required=True, example="tami"),
    'user_role': fields.List(fields.String, example=("admin", "super_user")),
    'user_email': fields.String(request=True, example="itri@kuohwa.com")
})

add_account_output_payload = api.clone(u'add帳號output', base_input_payload)

delete_input_payload = api.model(u'delete帳號input', {
    'user_account': fields.String(required=True, example="tami"),
})

delete_output_payload = api.clone(u'delete帳號output', base_input_payload)

get_account_data = api.model('get_data', {
    'user_account': fields.String(required=True, default="tami"),
    'user_role': fields.List(fields.String, default=["admin", "super_user"]),
    'user_email': fields.String(required=True, default="itri@kuohwa.com"),
    'update_time': fields.String(required=True, default="")
})

get_account_input_payload = api.model(u'get帳號input', {})

get_account_output_payload = api.clone(u'get帳號output', base_input_payload,
                                       {
                                           'data': fields.List(fields.Nested(get_account_data))
                                       })

update_account_data = api.model('update_data', {
    'new_user_account': fields.String(required=True, default="tami"),
    'new_user_role': fields.List(fields.String, example=("admin", "super_user")),
    'new_user_email': fields.String(required=True, default="itri@kuohwa.com")
})

update_account_input_payload = api.model(u'update帳號input', {
    'old_user_account': fields.String(required=True, example="tami"),
    'user_data': fields.Nested(update_account_data)
})

update_account_output_payload = api.clone(
    u'update帳號output', base_input_payload)
