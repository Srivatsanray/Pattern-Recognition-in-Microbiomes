import pandas as pd
import streamlit as st


def process_csv(data):
    data = pd.read_csv(data, sep=" ")
    data.index.name = "Otu"
    data = data.reset_index()
    data['Otu'] = data['Otu'].astype(str)
    data.drop(columns=data.columns[data.isnull().all()], inplace=True)
    return data


def merge_duplicate_columns(data):
    duplicates = data.columns.duplicated(keep=False)
    for dup_col in data.columns[duplicates]:
        data[dup_col] = data[data.columns[data.columns == dup_col]].apply(lambda x: ', '.join(x.dropna().astype(str)),
                                                                          axis=1)
    data = data.loc[:, ~duplicates]
    null_cols = data.columns[data.isnull().all()]
    data.drop(columns=null_cols, inplace=True)

    return data


def drop_columns(data, columns, indice):
    columns.remove(indice)
    data = data.drop(columns=columns)
    data[indice] = data[indice].str[4:]
    data = data.groupby(data[indice]).sum()
    data = data.transpose()
    data = data.reset_index()
    data = data.rename(columns={'index': 'Sample'})
    data = merge_duplicate_columns(data)
    return data


@st.cache_resource
def merge_operations(data, tax):
    data = pd.merge(data, tax, on=data.columns[0], how='inner')
    return data
