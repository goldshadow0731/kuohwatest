
from logging import exception
from typing_extensions import ParamSpec
from flask.globals import request
from utils.orcl_utils import OracleAccess
from email.mime.multipart import MIMEMultipart
from email .mime.text import MIMEText
from configs.tbl_consts import TBL_USER_ACCOUNT
import smtplib
import random,string,hashlib,datetime

class Account(object):

    @staticmethod
    def login(user_email, user_passwd):
        
        raw = OracleAccess.query(
            f'select EMAIL,PASSWD_SHA from  {TBL_USER_ACCOUNT} where EMAIL= :1', [user_email])
        if raw:
            passwd_sha = hashlib.sha256(str(user_passwd).encode('utf-8')).hexdigest()
            if(passwd_sha == raw[0][1]):
                return {
                    "message": "登入成功",
                    "RESULT": "0"
                }
            return {
                    "message": "登入失敗",
                    "RESULT": "1"
                }

        return {
            "message": "無此帳號",
            "RESULT": '1'
        }

    @staticmethod
    def forget(user_account):

        PASSWORD = ''.join(random.choice(
            string.ascii_letters + string.digits) for x in range(10))
        passwd_sha=hashlib.sha256(PASSWORD.encode('utf-8')).hexdigest()
        update_time=datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        raw = OracleAccess.query(
            f'select USER_ACCOUNT from {TBL_USER_ACCOUNT} where USER_ACCOUNT= :1', [user_account])
        print(raw)
        if raw:
            print(passwd_sha)
            OracleAccess.execute(
                f'update {TBL_USER_ACCOUNT} set PASSWD_SHA= :1,PASSWD=:2,UPDATE_TIME=:3 where USER_ACCOUNT= :4'
                , (passwd_sha,PASSWORD,update_time, user_account))
            content = MIMEMultipart()
            content["subject"] = 'New Password'
            content["from"] = 'asd599893@gmail.com'
            content["to"] = 'asd599893@gmail.com'
            content.attach(MIMEText('Your new password is' +
                                    PASSWORD+'.', 'plain', 'utf-8'))
            with smtplib.SMTP(host="smtp.gmail.com", port='587') as smtp:
                try:
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    smtp.login("asd599893@gmail.com",
                               "xtrtzibbbghjuknn")  # 登入寄件者gmail
                    smtp.send_message(content)  # 寄送郵件
                except Exception as e:
                    return("Error message: ", e)

            return {
                "message": "更改成功",
                "RESULT": "0"
            }
        return {
            "message": "更改失敗",
            "RESULT": '1'
        }

    @staticmethod
    def add_account(user_account, user_role, user_email):
        create_time=datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        n_role = ','.join(user_role)
        raw = OracleAccess.query(f'SELECT * FROM {TBL_USER_ACCOUNT} WHERE USER_ACCOUNT=:1',[user_account])
        if raw==[]:
            OracleAccess.insert(
            f'INSERT INTO {TBL_USER_ACCOUNT}(USER_ACCOUNT,ROLE,EMAIL,CREATE_TIME) values (:1,:2,:3,:4)'
            , [(user_account, n_role, user_email,create_time)])
            return {
                "message": "註冊成功",
                "RESULT": "0"
            }
        return {
            "message": "此帳號已被註冊",
            "RESULT": "1"
        }

    @ staticmethod
    def delete_account(user_account):
        raw = OracleAccess.query(
            f'select USER_ACCOUNT from  {TBL_USER_ACCOUNT} where USER_ACCOUNT= :user_id', [user_account])
        print(raw)
        if raw:
            OracleAccess.execute(
                f'delete from {TBL_USER_ACCOUNT} where USER_ACCOUNT= :1', [(user_account)])
            return {
                "message": "刪除成功",
                "RESULT": "0"
            }
        return {
            "message": "未有此帳號",
            "RESULT": "1"
        }

    @ staticmethod
    def get_account():
        raws = OracleAccess.query(
            f'select * from  {TBL_USER_ACCOUNT}')
        tmp_data = []
        if raws:
            for raw in raws:
                tmp_data.append({
                    "user_account": raw[0],
                    "user_email": raw[1],
                    "user_role": raw[3].split(',') if raw[3] else [],
                    "update_time": raw[4]
                })
            return {
                "message": "讀取成功",
                "RESULT": "0",
                "data": tmp_data
            }
        return {
            "message": "讀取成功",
            "RESULT": "1"
        }

    @ staticmethod
    def update_account(old_user_account, new_user_account, new_user_role, new_user_email):
        update_time=datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        n_role = ','.join(new_user_role)
        raw = OracleAccess.query(
            f'select USER_ACCOUNT from  {TBL_USER_ACCOUNT} where USER_ACCOUNT= :user_account', [old_user_account])
        if raw:
            OracleAccess.execute(
                f'update {TBL_USER_ACCOUNT} set USER_ACCOUNT= :1 , ROLE= :2 , EMAIL= :3 ,UPDATE_TIME=:4 where USER_ACCOUNT= :5',
                (new_user_account, n_role, new_user_email,update_time, old_user_account))
            return {
                "message": "更新成功",
                "RESULT": "0"
            }
        return {
            "message": "更新失敗",
            "RESULT": "1"
        }
