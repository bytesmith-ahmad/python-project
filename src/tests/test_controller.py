import sys, os ; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from pypika import Query, Table, Field
from business.controller import Controller
from business.models.otolith import Otolith
from persistence.datastore import DataStore

# Mocked data for testing
table_mock = MagicMock()
columns_mock = MagicMock()
data_mock = MagicMock()

# Test cases for the Controller class

def test_establish_connection():
    path_to_db = "test.db"
    Controller.establish_connection(path_to_db)
    assert Controller.db is not None
    assert isinstance(Controller.db, DataStore)

def test_get_tables():
    with patch.object(DataStore, 'get_tables', return_value=["Table1", "Table2"]) as mock_method:
        tables = Controller.get_tables()
        assert tables == ["Table1", "Table2"]

def test_execute_script():
    script = ["SELECT * FROM table;", "INSERT INTO table VALUES (1, 'name');"]
    with patch.object(DataStore, 'execute_script', return_value="Script executed successfully.") as mock_execute_script:
        result = Controller.execute_script(script)
        mock_execute_script.assert_called_once_with("\n".join(script))
        assert result == "Script executed successfully."
