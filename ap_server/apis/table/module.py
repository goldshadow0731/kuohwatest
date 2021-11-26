from flask_mail import Message

import base_api
from configs.tbl_consts import TBL_USER_DETECT_TABLE, TBL_USER_IMAGE_PATH_TABLE, TBL_USER_MAPPING_TABLE
from utils.orcl_utils import OracleAccess


class Table(object):
    @staticmethod
    def autosave_detect_table(uuid, data):  # 表格偵測自動儲存 API
        raw = OracleAccess.insert(
            f"insert into {TBL_USER_DETECT_TABLE} (UUID, UPPER_LEFT, UPPER_RIGHT, LOWER_LEFT, LOWER_RIGHT, CELL_NAME, CELL_UPPER_LEFT, CELL_UPPER_RIGHT, CELL_LOWER_LEFT, CELL_LOWER_RIGHT, START_ROW, END_ROW, START_COL, END_COL, CONTENT) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)", [(uuid, data['page_number']['table_id']['upper_left'], data['page_number']['table_id']['upper_right'], data['page_number']['table_id']['lower_left'], data['page_number']['table_id']['lower_right'], data['page_number']['table_id']['cells'][0]['name'], data['page_number']['table_id']['cells'][0]['upper_left'], data['page_number']['table_id']['cells'][0]['upper_right'], data['page_number']['table_id']['cells'][0]['lower_left'], data['page_number']['table_id']['cells'][0]['lower_right'], data['page_number']['table_id']['cells'][0]['start_row'], data['page_number']['table_id']['cells'][0]['end_row'], data['page_number']['table_id']['cells'][0]['start_col'], data['page_number']['table_id']['cells'][0]['end_col'], data['page_number']['table_id']['cells'][0]['content'])])
        result = {
            'result': 0,
            'message': ""
        }
        return result

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
        result = {
            'result': 0,
            'message': "",
            'data': data
        }
        return result

    @staticmethod
    def get_key_value_mapping(vendor, file_type):  # ERP Key-Value 對照表 API
        raw = OracleAccess.query(
            f"select * from {TBL_USER_MAPPING_TABLE} where VENDOR = '{vendor}' and FILE_TYPE = '{file_type}'")
        data = {}
        if raw:
            for raw_data in raw:
                data[raw_data[0]] = [
                    field_value for field_value in raw_data[1].split(",")]
        result = {
            'result': 0,
            'message': "",
            'data': data
        }
        return result

    @staticmethod
    def autosave_key_value_mapping(data):  # 單元格偵測自動儲存 API
        for raw_data in data:
            fieldvalue = ",".join(raw_data['fieldvalue'])
            raw = OracleAccess.insert(
                f"insert into {TBL_USER_MAPPING_TABLE} (FIELD, FIELDVALUE, VENDOR, FILE_TYPE) values (:1, :2, :3, :4)", [(raw_data['field'], fieldvalue, raw_data['vendor'], raw_data['file_type'])])
        result = {
            'result': 0,
            'message': "test autosave_key_value_mapping"
        }
        return result

    @staticmethod
    def get_image_path(uuid):  # 圖片路徑 API
        raw = OracleAccess.query(
            f"select * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}'")
        data = {
            "uuid": raw[0][0],
            "front_path": raw[0][1],
            "back_path": raw[0][2]
        }
        result = {
            'result': 0,
            'message': "",
            'data': data
        }
        return result
