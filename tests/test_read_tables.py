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


def test_add_two_series_none():
    
    s0 = pd.Series([0, 1, 2, 3])
    s1 = pd.Series([3, 2, 1, None])
    
    result_series = read_table.add_two_series(s0, s1)
    
    assert len(result_series) == len(s0)
    
    expected = pd.Series([3.0, 3.0, 3.0, 3.0])
    
    assert result_series.equals(expected), result_series


def test_add_series_missing():
    
    i0 = pd.Series(['a', 'b', 'c', 'd'])
    i1 = pd.Series(['a', 'b', 'c'])
    s0 = pd.Series([0, 1, 2, 3], index=i0)
    s1 = pd.Series([3, 2, 1], index=i1)
    
    result_series = read_table.add_two_series(s0, s1)
    
    assert len(result_series) == len(s0)
    
    expected = pd.Series([3.0, 3.0, 3.0, 3.0], index=i0)
    
    assert result_series.equals(expected), result_series


def test_add_columns_missing():
    i0 = pd.Series(['a', 'b', 'c', 'd'])
    i1 = pd.Series(['a', 'b', 'c'])
    s0 = pd.Series([0, 1, 2, 3], index=i0)
    s1 = pd.Series([3, 2, 1], index=i1)

    d0 = pd.DataFrame(s0, index=i0, columns=['count'])
    d1 = pd.DataFrame(s1, index=i1, columns=['count'])
    
    result_df = read_table.add_columns(d0, d1)
    
    assert len(result_df) == len(s0)
    
    expected = pd.DataFrame([3.0, 3.0, 3.0, 3.0], index=i0, columns=['count'])
    
    assert result_df.equals(expected), result_df


if "__main__" == __name__:
    pytest.main()
