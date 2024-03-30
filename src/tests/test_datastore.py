import pytest, sqlite3
from unittest.mock import MagicMock, patch
from persistence.datastore import DataStore
from pypika import Query, Table, Field

# Mocked data for testing
db_path_mock = MagicMock()
table_mock = MagicMock()
sql_mock = MagicMock()
rows_mock = MagicMock()

# Test cases for the DataStore class

def test_connect():
        data_store = DataStore()
        data_store.connect(':memory:')
        row = data_store.connection.execute("SELECT sqlite_version()").fetchone()
        for v in row:
            assert v == '3.43.1'

def test_close():
    data_store = DataStore()
    data_store.connection = MagicMock()
    result = data_store.close()
    data_store.connection.close.assert_called_once()
    assert result == "Closed"

def test_commit():
    data_store = DataStore()
    data_store.connection = MagicMock()
    result = data_store.commit()
    data_store.connection.commit.assert_called_once()
    assert result == "Changes saved"

def test_get_tables():
    data_store = DataStore()
    data_store.connection = MagicMock()
    data_store.connection.execute.return_value.fetchall.return_value = [("Table1",), ("Table2",)]
    tables = data_store.get_tables()
    assert isinstance(tables, list)
    assert len(tables) == 2
    assert isinstance(tables[0], Table)
    assert isinstance(tables[1], Table)

def test_get_fields():
    data_store = DataStore()
    data_store.connection = MagicMock()
    data_store.connection.execute.return_value.fetchall.return_value = [("Field1",), ("Field2",)]
    fields = data_store.get_fields(table_mock)
    assert isinstance(fields, list)
    assert len(fields) == 2
    assert isinstance(fields[0], Field)
    assert isinstance(fields[1], Field)

def test_execute_script():
    data_store = DataStore()
    data_store.connection = MagicMock()
    result = data_store.execute_script("script")
    data_store.connection.executescript.assert_called_once_with("script")
    assert result == "Script executed without errors"

def test_reveal():
    data_store = DataStore()
    rows = [MagicMock(), MagicMock()]
    rows[0].keys.return_value = ["key1", "key2"]
    rows[0].__getitem__.side_effect = lambda key: {"key1": "value1", "key2": "value2"}[key]
    rows[1].keys.return_value = ["key1", "key2"]
    rows[1].__getitem__.side_effect = lambda key: {"key1": "value3", "key2": "value4"}[key]
    result = data_store.reveal(rows)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert isinstance(result[1], dict)
    assert result[0] == {"key1": "value1", "key2": "value2"}
    assert result[1] == {"key1": "value3", "key2": "value4"}