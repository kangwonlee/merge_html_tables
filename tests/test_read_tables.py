import itertools
import os
import sys
import tempfile

import pandas as pd
import pytest


sys.path.insert(
    0, 
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),os.pardir
        )
    )
)

import read_table


def test_read_table():

    data = [
        ["a1", "b1 author1 Search 21", "Attach1", "d1"],
        ["a2", "b2 author2 Search 22", "Attach2", "d2"],
        ["a3", "b3 author3 Search 23", "Attach3", "d3"],
        ["a4", "b4 author4 Search 24", "Attach4", "d4"],
    ]
    columns = ["No", "Title", "Attach", "Published"]

    input_table = pd.DataFrame(data, columns=columns, index=range(4))

    with tempfile.NamedTemporaryFile(mode='w+t') as fp_sample_html:
        input_table.to_html(fp_sample_html)
        fp_sample_html.seek(0)

        result = read_table.read_table(fp_sample_html)

    assert isinstance(result, pd.DataFrame)
    assert 'subject' in result.columns
    assert 'author' in result.columns
    assert 'count' in result.columns
    assert 'Attach' in result.columns
    assert 'Published' in result.columns


def test_gen_files():
    name_list = ['abc', 'def', 'ghi']
    ext_list = ['.html', '.xls']

    filename_list = [name + ext for name, ext in itertools.product(name_list, ext_list)]

    result = list(read_table.gen_files(filename_list=filename_list, ext='html', pattern="abc"))

    assert 'abc.html' in result


if "__main__" == __name__:
    pytest.main()
