from flask_mail import Message

import base_api
from configs.tbl_consts import TBL_USER_ACCOUNT
from utils.orcl_utils import OracleAccess


class Account(object):
    @staticmethod
    def login(username, passwd):  # 登入 API
        # TODO
        # raw = OracleAccess.query("select * from test")
        return {
            'result': 0,
            'message': "",
            "data": "登入成功",
            "test": "123"
        }

    @staticmethod
    def forget(username):  # 忘記密碼 API
        raw = OracleAccess.query(
            f"select EMAIL from {TBL_USER_ACCOUNT} where USER_ID = '{username}'")
        if raw[0][0]:
            msg = Message("title", recipients=[raw[0][0]])
            msg.body = "content"
            base_api.mail.send(msg)
            result = {
                'result': 0,
                'message': ""
            }
        else:
            result = {
                'result': 1,
                'message': ""
            }
        return result

    @staticmethod
    def get_account_list():  # 帳號清單 API
        data = []
        raw = OracleAccess.query(f"select * from {TBL_USER_ACCOUNT}")
        if raw:
            for user in raw:
                data.append({
                    "user_id": str(user[0]),
                    "role": [role for role in user[1].split(',')],
                    "email": user[2],
                    "update_time": user[4]
                })
        result = {
            'result': 0,
            'message': "",
            'data': data
        }
        return result

    @ staticmethod
    def add_account_list(user_id, role, email):  # 新增帳號清單 API
        role = ",".join(role)
        raw = OracleAccess.insert(
            f"insert into {TBL_USER_ACCOUNT} (USER_ID, ROLE, EMAIL) values (:1, :2, :3)", [(user_id, role, email)])
        result = {
            'result': 0,
            'message': ""
        }
        return result

    @ staticmethod
    def delete_account_list(user_id):  # 刪除帳號清單 API
        OracleAccess.execute(
            f"delete from {TBL_USER_ACCOUNT} where USER_ID = '{user_id}'", args=[])
        result = {
            'result': 0,
            'message': ""
        }
        return result

    @ staticmethod
    def update_account_list(old_user_id, data):  # 更新帳號清單 API
        new_role = ",".join(data['new_role'])
        new_user_id = data["new_user_id"]
        new_email = data["new_email"]
        raw = OracleAccess.execute(
            f"update {TBL_USER_ACCOUNT} set USER_ID = '{new_user_id}', ROLE = '{new_role}', EMAIL = '{new_email}' where USER_ID = '{old_user_id}'", args=[])
        result = {
            'result': 0,
            'message': ""
        }
        return result
