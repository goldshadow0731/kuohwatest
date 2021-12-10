from werkzeug.datastructures import FileStorage
import unittest
import pytest
import os

import json
from tests.base import BaseTestCase
from utils.orcl_utils import OracleAccess
from configs.tbl_consts import TBL_USER_DETECT_TABLE, TBL_USER_IMAGE_PATH_TABLE, TBL_USER_MAPPING_TABLE


@pytest.fixture
def client():
    app = BaseTestCase.create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_autosave_detect_table(client, mocker):
    is_exist = False

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_DETECT_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_detect_table',
        data=json.dumps({
            "uuid": "sa5e122hy215cb3degrt",
            "data": {
                "page_number": {
                    "table_id": {
                        "upper_left": "99,82",
                        "upper_right": "99,857",
                        "lower_right": "2356,857",
                        "lower_left": "2356,82",
                        "cells": [
                            {
                                "name": "cell_id1",
                                "upper_left": "99,82",
                                "upper_right": "99,857",
                                "lower_right": "2356,857",
                                "lower_left": "2356,82",
                                "start_row": 0,
                                "end_row": 2,
                                "start_col": 0,
                                "end_col": 3,
                                "content": "example"
                            }
                        ]
                    }
                }
            }
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_detect_table(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["s5weqw183cwqe75dd", "99,82", "99,857", "2356,82", "2356,857", "cell_id1", "99,82", "99,857", "2356,82", "2356,857", "0", "2", "0", "3", "example"]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_detect_table',
        data=json.dumps({
            "uuid": "s5weqw183cwqe75dd"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'No data'
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        'page_number': {
            'table_id': {
                'lower_left': None,
                'lower_right': None,
                'upper_left': None,
                'upper_right': None,
                'cells': None
            }
        }
    }

    response = client.post(
        '/api/table/get_detect_table',
        data=json.dumps({
            "uuid": "s5weqw183cwqe75dd"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "page_number": {
            "table_id": {
                "upper_left": "99,82",
                "upper_right": "99,857",
                "lower_right": "2356,857",
                "lower_left": "2356,82",
                "cells": [{
                    "name": "cell_id1",
                    "upper_left": "99,82",
                    "upper_right": "99,857",
                    "lower_right": "2356,857",
                    "lower_left": "2356,82",
                    "start_row": 0,
                    "end_row": 2,
                    "start_col": 0,
                    "end_col": 3,
                    "content": "example"
                }]
            }
        }
    }


def test_get_key_value_mapping(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["epr_key1", "Bo,Borad,Boardnum"], ["epr_key4", "sta,status,status1"]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_key_value_mapping',
        data=json.dumps({
            "vendor": "aa",
            "file_type": "bb"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'No match data'
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {}

    response = client.post(
        '/api/table/get_key_value_mapping',
        data=json.dumps({
            "vendor": "aa",
            "file_type": "bb"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "epr_key1": [
            "Bo",
            "Borad",
            "Boardnum"
        ],
        "epr_key4": [
            "sta",
            "status",
            "status1"
        ]
    }


def test_autosave_key_value_mapping(client, mocker):
    is_exist = False

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_MAPPING_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_key_value_mapping',
        data=json.dumps({"data": [{
            "field": "epr_key1",
            "fieldvalue": [
                "Bo",
                "Borad"
            ],
            "vendor": "",
            "file_type": ""
        }]}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_image_path(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["s5weqw183cwqe75dd", "../storage/photo/s5weqw183cwqe75dd/front.jpg", "../storage/photo/s5weqw183cwqe75dd/end.jpg"]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_image_path',
        data=json.dumps({"uuid": ""}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'wrong uuid'
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        'uuid': None,
        'front_path': None,
        'back_path': None
    }

    response = client.post(
        '/api/table/get_image_path',
        data=json.dumps({"uuid": ""}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "uuid": "s5weqw183cwqe75dd",
        "front_path": "../storage/photo/s5weqw183cwqe75dd/front.jpg",
        "back_path": "../storage/photo/s5weqw183cwqe75dd/end.jpg"
    }


def test_autosave_image_path(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["s5weqw183cwqe75dd", "../storage/photo/s5weqw183cwqe75dd/front.jpg", "../storage/photo/s5weqw183cwqe75dd/end.jpg"]]

    def _execute(sql, *args, **kwargs):
        if TBL_USER_IMAGE_PATH_TABLE in sql:
            return []

    mocker.patch.object(OracleAccess, "query", _query)
    mocker.patch.object(OracleAccess, "execute", _execute)
    with open(os.path.join("./20211209_151708.jpg"), 'rb') as f:
        front_image = FileStorage(
            stream=f.read(),
            filename="front.jpg",
            content_type="image/jpeg"
        )
    with open(os.path.join("./20211209_151713.jpg"), 'rb') as f:
        back_image = FileStorage(
            stream=f.read(),
            filename="back.jpg",
            content_type="image/jpeg"
        )

    response = client.post(
        '/api/table/autosave_image_path',
        data={
            "front_path": front_image,
            "back_path": back_image
        },
        content_type="multipart/form-data"
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True

    response = client.post(
        '/api/table/autosave_image_path',
        data={
            "front_path": front_image,
            "back_path": back_image
        },
        content_type='multipart/form-data'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
