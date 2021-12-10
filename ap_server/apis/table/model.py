from flask_restplus import Namespace, Resource, fields, model
from werkzeug.datastructures import FileStorage

api = Namespace("table", description=u"表格偵測結構", ordered=False)


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})


# 表格偵測自動儲存 API
table_autosaveDetectTable_input_tier4_data_payload = api.model(u'表格偵測自動儲存input_tier4_data',  {
    "name": fields.String(required=True, example="cell_id1"),
    "upper_left": fields.String(required=True, example="99,82"),
    "upper_right": fields.String(required=True, example="99,857"),
    "lower_right": fields.String(required=True, example="2356,857"),
    "lower_left": fields.String(required=True, example="2356,82"),
    "start_row": fields.Integer(required=True, example=0),
    "end_row": fields.Integer(required=True, example=2),
    "start_col": fields.Integer(required=True, example=0),
    "end_col": fields.Integer(required=True, example=3),
    "content": fields.String(required=True, example="example"),
})

table_autosaveDetectTable_input_tier3_data_payload = api.model(u'表格偵測自動儲存input_tier3_data',  {
    "upper_left": fields.String(required=True, example="99,82"),
    "upper_right": fields.String(required=True, example="99,857"),
    "lower_right": fields.String(required=True, example="2356,857"),
    "lower_left": fields.String(required=True, example="2356,82"),
    "cells": fields.List(fields.Nested(table_autosaveDetectTable_input_tier4_data_payload))
})

table_autosaveDetectTable_input_tier2_data_payload = api.model(u'表格偵測自動儲存input_tier2_data',  {
    "table_id": fields.Nested(table_autosaveDetectTable_input_tier3_data_payload)
})

table_autosaveDetectTable_input_tier1_data_payload = api.model(u'表格偵測自動儲存input_tier1_data',  {
    "page_number": fields.Nested(table_autosaveDetectTable_input_tier2_data_payload)
})

table_autosaveDetectTable_input_payload = api.model(u'表格偵測自動儲存input',  {
    "uuid": fields.String(required=True, example="sa5e122hy215cb3degrt"),
    "data": fields.Nested(table_autosaveDetectTable_input_tier1_data_payload)
})

table_autosaveDetectTable_output_payload = api.clone(
    u'表格偵測自動儲存output', base_input_payload)


# 表格偵測 API
table_getDetectTable_input_payload = api.model(u'表格偵測input',  {
    "uuid": fields.String(required=True, example="s5weqw183cwqe75dd")
})

table_getDetectTable_output_tier4_data_payload = api.model(u'表格偵測output_tier4_data',  {
    "name": fields.String(required=True, example="cell_id1"),
    "upper_left": fields.String(required=True, example="99,82"),
    "upper_right": fields.String(required=True, example="99,857"),
    "lower_right": fields.String(required=True, example="2356,857"),
    "lower_left": fields.String(required=True, example="2356,82"),
    "start_row": fields.Integer(required=True, example=0),
    "end_row": fields.Integer(required=True, example=2),
    "start_col": fields.Integer(required=True, example=0),
    "end_col": fields.Integer(required=True, example=3),
    "content": fields.String(required=True, example="example"),
})

table_getDetectTable_output_tier3_data_payload = api.model(u'表格偵測output_tier3_data',  {
    "upper_left": fields.String(required=True, example="99,82"),
    "upper_right": fields.String(required=True, example="99,857"),
    "lower_right": fields.String(required=True, example="2356,857"),
    "lower_left": fields.String(required=True, example="2356,82"),
    "cells": fields.List(fields.Nested(table_getDetectTable_output_tier4_data_payload))
})

table_getDetectTable_output_tier2_data_payload = api.model(u'表格偵測output_tier2_data',  {
    "table_id": fields.Nested(table_getDetectTable_output_tier3_data_payload)
})

table_getDetectTable_output_tier1_data_payload = api.model(u'表格偵測output_tier1_data',  {
    "page_number": fields.Nested(table_getDetectTable_output_tier2_data_payload)
})

table_getDetectTable_output_payload = api.clone(u'表格偵測output', base_input_payload, {
    'data': fields.Nested(table_getDetectTable_output_tier1_data_payload)
})


# ERP Key-Value 對照表 API
table_getKeyValueMapping_input_payload = api.model(u'ERP Key-Value 對照表input',  {
    "vendor": fields.String(required=True, example=""),
    "file_type": fields.String(required=True, example="")
})

table_getKeyValueMapping_output_payload = api.clone(u'ERP Key-Value 對照表output', base_input_payload, {
    'data': fields.Raw()
})


# 單元格偵測自動儲存 API
table_autosaveKeyValueMapping_input_data_payload = api.model(u'單元格偵測自動儲存input_data',  {
    "field": fields.String(required=True, example="epr_key1"),
    "fieldvalue": fields.List(fields.String, required=True, example=["Bo", "Borad"]),
    "vendor": fields.String(required=True, example=""),
    "file_type": fields.String(required=True, example="")
})

table_autosaveKeyValueMapping_input_payload = api.model(u'單元格偵測自動儲存input',  {
    "data": fields.List(fields.Nested(table_autosaveKeyValueMapping_input_data_payload))
})

table_autosaveKeyValueMapping_output_payload = api.clone(
    u'單元格偵測自動儲存output', base_input_payload)


# 圖片路徑 API
table_getImagePath_input_payload = api.model(u'圖片路徑input',  {
    "uuid": fields.String(required=True, example="")
})

table_getImagePath_output_data_payload = api.model(u'圖片路徑output_data',  {
    "uuid": fields.String(required=True, example=""),
    "front_path": fields.String(required=True, example=""),
    "back_path": fields.String(required=True, example="")
})

table_getImagePath_output_payload = api.clone(u'圖片路徑output', base_input_payload, {
    'data': fields.Nested(table_getImagePath_output_data_payload)
})


# 自動儲存圖片路徑 API
table_autosavImagePath_input_payload = api.parser()
table_autosavImagePath_input_payload.add_argument(
    'front_path', type=FileStorage, location='files')
table_autosavImagePath_input_payload.add_argument(
    'back_path', type=FileStorage, location='files')

table_autosavImagePath_output_payload = api.clone(
    u'自動儲存圖片路徑output', base_input_payload)
