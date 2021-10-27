from apis.account.model import *
from apis.account.module import *
from flask import session
from base_api import CustomResource

ROLE_ADMIN = "Admin"


@api.route("/login")
class Login(CustomResource):
    @api.expect(login_input_payload)
    @api.marshal_with(login_output_payload)
    def post(self):
        session["roles"] = [ROLE_ADMIN]
        data = api.payload
        return Account.login(user_email=data["user_email"], user_passwd=data["user_passwd"])


@api.route("/forget")
class Forget(CustomResource):
    @api.expect(forget_input_payload)
    @api.marshal_with(forget_output_payload)
    def post(self):
        data = api.payload
        return Account.forget(user_account=data["user_account"])


@api.route("/add_account_list")
class Add_account(CustomResource):
    @api.expect(add_account_input_payload)
    @api.marshal_with(add_account_output_payload)
    def post(self):
        data = api.payload
        return Account.add_account(user_account=data["user_account"], user_role=data["user_role"], user_email=data["user_email"])


@api.route("/delete_account_list")
class Delete_account(CustomResource):
    @api.expect(delete_input_payload)
    @api.marshal_with(delete_output_payload)
    def post(self):
        data = api.payload
        return Account.delete_account(user_account=data["user_account"])


@api.route("/get_account_list")
class Get_account(CustomResource):
    @api.expect(get_account_input_payload)
    @api.marshal_with(get_account_output_payload)
    def post(self):
        data = api.payload
        return Account.get_account()


@api.route("/update_account_list")
class Update_account(CustomResource):
    @api.expect(update_account_input_payload)
    @api.marshal_with(update_account_output_payload)
    def post(self):
        data = api.payload
        payload_data = data["user_data"]
        return Account.update_account(old_user_account=data['old_user_account'],
                                      new_user_account=payload_data["new_user_account"],
                                      new_user_role=payload_data["new_user_role"],
                                      new_user_email=payload_data["new_user_email"])
