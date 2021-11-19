from flask_restplus import Namespace, Resource, fields, model

api = Namespace("account", description=u"帳號及權限管理")


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})

# 登入 API
account_input_payload = api.model(u'帳號input', {
    'username': fields.String(required=True, example="tami"),
    'passwd': fields.String(required=True, example="tami")
})

account_output_payload = api.clone(u'帳號output', base_input_payload, {
    'data': fields.String(required=True),
    "test": fields.String(required=True)
})


# 忘記密碼 API
account_forget_input_payload = api.model(u'忘記密碼input', {
    'username': fields.String(required=True, example="tami")
})

account_forget_output_payload = api.clone(u'忘記密碼output', base_input_payload)


# 帳號清單 API
account_getAccountList_output_data_payload = api.model(u'帳號清單output_data', {
    "user_id": fields.String(required=True, example="1"),
    "role": fields.List(fields.String, required=True, example=["admin", "super_user"]),
    "email": fields.String(required=True, example="test@gmail.com"),
    "update_time": fields.String(required=True, example="2021/07/29")
})

account_getAccountList_output_payload = api.clone(u'帳號清單output', base_input_payload, {
    'data': fields.List(fields.Nested(account_getAccountList_output_data_payload), required=True)
})


# 新增帳號清單 API
account_addAccountList_input_payload = api.model(u'新增帳號清單input',  {
    "user_id": fields.String(required=True, example="1"),
    "role": fields.List(fields.String, required=True, example=["admin", "super_user"]),
    "email": fields.String(required=True, example="test@gmail.com")
})

account_addAccountList_output_payload = api.clone(
    u'新增帳號清單output', base_input_payload)

# 刪除帳號清單 API
account_deleteAccountList_input_payload = api.model(u'刪除帳號清單input',  {
    "user_id": fields.String(required=True, example="1")
})

account_deleteAccountList_output_payload = api.clone(
    u'刪除帳號清單output', base_input_payload)

# 更新帳號清單 API
account_updateAccountList_input_data_payload = api.model(u'更新帳號清單input_data',  {
    "new_user_id": fields.String(required=True, example="2"),
    "new_role": fields.List(fields.String, required=True, example=["admin", "super_user"]),
    "new_email": fields.String(required=True, example="test@gmail.com")
})

account_updateAccountList_input_payload = api.model(u'更新帳號清單input',  {
    "old_user_id": fields.String(required=True, example="1"),
    "data": fields.Nested(account_updateAccountList_input_data_payload)
})

account_updateAccountList_output_payload = api.clone(
    u'更新帳號狀態output', base_input_payload)
