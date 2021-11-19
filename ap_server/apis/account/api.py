from apis.account.model import *
from apis.account.module import *
from flask import session
from base_api import CustomResource

ROLE_ADMIN = "Admin"


@api.route("/test")
class Login2(CustomResource):
    allow_roles = [ROLE_ADMIN]

    def post(self):
        print(api.payload)
        return "OK"


@api.route("/login")  # 登入 API
class Login(CustomResource):
    @api.expect(account_input_payload)
    @api.marshal_with(account_output_payload)
    def post(self):
        session["roles"] = [ROLE_ADMIN]
        data = api.payload
        return Account.login(username=data["username"], passwd=data["passwd"])


@api.route("/forget")  # 忘記密碼 API
class Forget(CustomResource):
    @api.expect(account_forget_input_payload)
    @api.marshal_with(account_forget_output_payload)
    def post(self):
        data = api.payload
        return Account.forget(username=data["username"])


@api.route("/get_account_list")  # 帳號清單 API
class GetAccountList(CustomResource):
    #　@api.expect(account_getAccountList_input_payload)
    @api.marshal_with(account_getAccountList_output_payload)
    def post(self):
        return Account.get_account_list()


@api.route("/add_account_list")  # 新增帳號清單 API
class AddAccountList(CustomResource):
    @api.expect(account_addAccountList_input_payload)
    @api.marshal_with(account_addAccountList_output_payload)
    def post(self):
        data = api.payload
        return Account.add_account_list(user_id=data["user_id"], role=data["role"], email=data["email"])


@api.route("/delete_account_list")  # 刪除帳號清單 API
class DeleteAccountList(CustomResource):
    @api.expect(account_deleteAccountList_input_payload)
    @api.marshal_with(account_deleteAccountList_output_payload)
    def post(self):
        data = api.payload
        return Account.delete_account_list(user_id=data["user_id"])


@api.route("/update_account_list")  # 更新帳號清單 API
class updateAccountList(CustomResource):
    @api.expect(account_updateAccountList_input_payload)
    @api.marshal_with(account_updateAccountList_output_payload)
    def post(self):
        data = api.payload
        return Account.update_account_list(old_user_id=data["old_user_id"], data=data["data"])
