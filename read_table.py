#%%
import os
import sys

import pandas as pd


#%%
def main(argv):
    in_file, out_file = argv[:2]

    table = read_table(in_file)

    table.to_excel(out_file)


#%%
def gen_files(filename_list=os.listdir(), ext=".html", pattern="ECA"):
    for filename in filename_list:
        base, ext = os.path.splitext(filename)
        if ext.endswith(ext) and (pattern in base):
            yield filename


#%%
def read_table(html_filename):
    return rebuild_table(read_html(html_filename))


#%%
def read_html(in_file : str) -> pd.DataFrame:
    table_list = pd.read_html(in_file, encoding="utf-8")
    table = table_list[0]
    table.set_index('No', inplace=True)
    return table

#%%
def split_count(table):
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.split.html
    return table['Title'].str.split(r"\s+Search\s+", n=1, expand=True)


#%%
def split_author(subject_author_count):
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.rsplit.html
    return subject_author_count[0].str.rsplit(r" ", n=1, expand=True)


#%%
def rebuild_table(table):
    subject_author_count = split_count(table)
    subject_author = split_author(subject_author_count)

    table['subject'] = subject_author[0]
    table['author'] = subject_author[1]
    # https://datatofish.com/string-to-integer-dataframe/
    table['count'] = subject_author_count[1].astype(int)

    # https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
    new_table = table[['subject', 'author', 'count', 'Attach', 'Published',]]

    return new_table


#%%
def get_rename_dict(df, postfix, key):
    columns = list(df.columns)
    columns.remove(key)

    return {item: item + '_' + postfix for item in columns}


#%%
def rename_table_columns(df, postfix, key):
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    return df.rename(columns=get_rename_dict(df, postfix, key))


#%%
def add_two_series(series0 : pd.Series, series1 : pd.Series, fill_value=0) -> pd.Series:
    return series0.add(series1, fill_value=fill_value)


#%%
def add_columns(table0 : pd.DataFrame, table1 : pd.DataFrame, column='count', fill_value=0):
    return pd.DataFrame(add_two_series(table0[column], table1[column], fill_value=fill_value))


#%%
if "__main__" == __name__:
    main(sys.argv[1:])

# More references :
# https://www.geeksforgeeks.org/python-pandas-split-strings-into-two-list-columns-using-str-split/
