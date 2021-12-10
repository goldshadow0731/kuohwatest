from flask import request
from flask_mail import Message
from werkzeug.utils import secure_filename
import os

import base_api
from configs.tbl_consts import TBL_USER_DETECT_TABLE, TBL_USER_IMAGE_PATH_TABLE, TBL_USER_MAPPING_TABLE
from utils.orcl_utils import OracleAccess


class Table(object):
    @staticmethod
    def autosave_detect_table(uuid, data):  # 表格偵測自動儲存 API
        OracleAccess.execute(
            f"""insert into {TBL_USER_DETECT_TABLE} (
                UUID, 
                UPPER_LEFT, 
                UPPER_RIGHT, 
                LOWER_LEFT, 
                LOWER_RIGHT, 
                CELL_NAME, 
                CELL_UPPER_LEFT, 
                CELL_UPPER_RIGHT, 
                CELL_LOWER_LEFT, 
                CELL_LOWER_RIGHT, 
                START_ROW, 
                END_ROW, 
                START_COL, 
                END_COL, 
                CONTENT) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)""", [(
                uuid,
                data['page_number']['table_id']['upper_left'],
                data['page_number']['table_id']['upper_right'],
                data['page_number']['table_id']['lower_left'],
                data['page_number']['table_id']['lower_right'],
                data['page_number']['table_id']['cells'][0]['name'],
                data['page_number']['table_id']['cells'][0]['upper_left'],
                data['page_number']['table_id']['cells'][0]['upper_right'],
                data['page_number']['table_id']['cells'][0]['lower_left'],
                data['page_number']['table_id']['cells'][0]['lower_right'],
                data['page_number']['table_id']['cells'][0]['start_row'],
                data['page_number']['table_id']['cells'][0]['end_row'],
                data['page_number']['table_id']['cells'][0]['start_col'],
                data['page_number']['table_id']['cells'][0]['end_col'],
                data['page_number']['table_id']['cells'][0]['content'])])
        return {
            'result': 0,
            'message': ""
        }

    @staticmethod
    def get_detect_table(uuid):  # 表格偵測 API
        raw = OracleAccess.query(
            f"select * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}'")
        if raw:
            data = {
                "page_number": {
                    "table_id": {
                        "upper_left": raw[0][1],
                        "upper_right": raw[0][2],
                        "lower_right": raw[0][4],
                        "lower_left": raw[0][3],
                        "cells": [{
                            "name": raw[0][5],
                            "upper_left": raw[0][6],
                            "upper_right": raw[0][7],
                            "lower_right": raw[0][9],
                            "lower_left": raw[0][8],
                            "start_row": int(raw[0][10]),
                            "end_row": int(raw[0][11]),
                            "start_col": int(raw[0][12]),
                            "end_col": int(raw[0][13]),
                            "content": raw[0][14]
                        }]
                    }
                }
            }
            return {
                'result': 0,
                'message': "",
                'data': data
            }
        return {
            'result': 1,
            'message': "No data",
            'data': {}
        }

    @staticmethod
    def get_key_value_mapping(vendor, file_type):  # ERP Key-Value 對照表 API
        raw = OracleAccess.query(
            f"select * from {TBL_USER_MAPPING_TABLE} where VENDOR = '{vendor}' and FILE_TYPE = '{file_type}'")
        if raw:
            data = {}
            for raw_data in raw:
                data[raw_data[0]] = [
                    field_value for field_value in raw_data[1].split(",")]
            return {
                'result': 0,
                'message': "",
                'data': data
            }
        return {
            'result': 1,
            'message': "No match data",
            'data': {}
        }

    @staticmethod
    def autosave_key_value_mapping(data):  # 單元格偵測自動儲存 API
        for raw_data in data:
            fieldvalue = ",".join(raw_data['fieldvalue'])
            raw = OracleAccess.execute(
                f"""insert into {TBL_USER_MAPPING_TABLE} (
                    FIELD, 
                    FIELDVALUE, 
                    VENDOR, 
                    FILE_TYPE) values (:1, :2, :3, :4)""", [(
                    raw_data['field'],
                    fieldvalue,
                    raw_data['vendor'],
                    raw_data['file_type'])])
        return {
            'result': 0,
            'message': ""
        }

    @staticmethod
    def get_image_path(uuid):  # 圖片路徑 API
        raw = OracleAccess.query(
            f"select * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}'")
        if raw:
            return {
                'result': 0,
                'message': "",
                'data': {
                    "uuid": raw[0][0],
                    "front_path": raw[0][1],
                    "back_path": raw[0][2]
                }
            }
        return {
            'result': 1,
            'message': "wrong uuid",
            'data': {}
        }

    @staticmethod
    def autosave_image_path(uuid):  # 圖片路徑 API
        if OracleAccess.query(f"select * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}'"):
            OracleAccess.execute(
                f"update {TBL_USER_IMAGE_PATH_TABLE} set FRONT_PATH = '', BACK_PATH = '' where UUID = '{uuid}'", args=[])
        else:
            OracleAccess.execute(
                f"insert into {TBL_USER_IMAGE_PATH_TABLE} (UUID, FRONT_PATH, BACK_PATH) values (:1, :2, :3)", [uuid, '', ''])

        root_path = os.environ.get(
            'nopath', "storage" if os.path.isdir("storage") else "../storage")
        user_path = os.path.join(root_path, 'photo', uuid)
        os.makedirs(user_path, exist_ok=True)

        if "front_path" in request.files:
            front_image = request.files["front_path"]
            front_path = os.path.join(user_path, secure_filename("front.jpg"))
            front_image.save(front_path)
            OracleAccess.execute(
                f"update {TBL_USER_IMAGE_PATH_TABLE} set FRONT_PATH = '{front_path}' where UUID = '{uuid}'", args=[])

        if "back_path" in request.files:
            back_image = request.files["back_path"]
            back_path = os.path.join(user_path, secure_filename("back.jpg"))
            back_image.save(back_path)
            OracleAccess.execute(
                f"update {TBL_USER_IMAGE_PATH_TABLE} set BACK_PATH = '{back_path}' where UUID = '{uuid}'", args=[])

        return {
            'result': 0,
            'message': ""
        }
