from apis.table.model import *
from apis.table.module import *
from flask import session
from base_api import CustomResource

ROLE_ADMIN = "Admin"


@api.route("/autosave_detect_table")  # 表格偵測自動儲存 API
class autosaveDetectTable(CustomResource):
    @api.expect(table_autosaveDetectTable_input_payload)
    @api.marshal_with(table_autosaveDetectTable_output_payload)
    def post(self):
        data = api.payload
        return Table.autosave_detect_table(uuid=data['uuid'], data=data['data'])


@api.route("/get_detect_table")  # 表格偵測 API
class getDetectTable(CustomResource):
    @api.expect(table_getDetectTable_input_payload)
    @api.marshal_with(table_getDetectTable_output_payload)
    def post(self):
        data = api.payload
        return Table.get_detect_table(uuid=data['uuid'])


@api.route("/get_key_value_mapping")  # ERP Key-Value 對照表 API
class getKeyValueMapping(CustomResource):
    @api.expect(table_getKeyValueMapping_input_payload)
    @api.marshal_with(table_getKeyValueMapping_output_payload)
    def post(self):
        data = api.payload
        return Table.get_key_value_mapping(vendor=data['vendor'], file_type=data['file_type'])


@api.route("/autosave_key_value_mapping")  # 單元格偵測自動儲存 API
class autosaveKeyValueMapping(CustomResource):
    @api.expect(table_autosaveKeyValueMapping_input_payload)
    @api.marshal_with(table_autosaveKeyValueMapping_output_payload)
    def post(self):
        data = api.payload
        return Table.autosave_key_value_mapping(data=data['data'])


@api.route("/get_image_path")  # 圖片路徑 API
class getImagePath(CustomResource):
    @api.expect(table_getImagePath_input_payload)
    @api.marshal_with(table_getImagePath_output_payload)
    def post(self):
        data = api.payload
        return Table.get_image_path(uuid=data['uuid'])


@api.route("/autosave_image_path")  # 自動儲存圖片路徑 API
class autosavImagePath(CustomResource):
    @api.expect(table_autosavImagePath_input_payload)
    @api.marshal_with(table_autosavImagePath_output_payload)
    def post(self):
        return Table.autosave_image_path(uuid="string")
