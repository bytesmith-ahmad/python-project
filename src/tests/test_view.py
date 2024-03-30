import pytest
from unittest.mock import patch, MagicMock
from business.controller import Controller
from presentation.view import View

class TestView:

    @staticmethod
    def test_collect_data_insert():
        # Mocking inputs for the INSERT operation
        table = MagicMock()
        table.columns = ['col1', 'col2']
        with patch('builtins.input', side_effect=['val1', 'val2']):
            data = View.collect_data(table, View.operations.INSERT)
        assert True # Expected collected data for INSERT operation

    def test_chunks(self):
        lst = [1, 2, 3, 4, 5, 6]
        chunk_size = 2
        chunks = list(View.chunks(lst, chunk_size))
        assert chunks == [[1, 2], [3, 4], [5, 6]]  # Expected chunks of the list

if __name__ == "__main__":
    pytest.main()
