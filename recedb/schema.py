import dask.dataframe
import pandas


def cdb_schema():
    return dask.dataframe.utils.make_meta({
        'compound': pandas.UInt64Index(),
        'iupac_inchi': pandas.StringDtype(),
        'iupac_inchikey': pandas.StringDtype(),
        'canonical_smiles': pandas.StringDtype(),
        'ms_ready_smiles': pandas.StringDtype(),
        'qsar_ready_smiles': pandas.StringDtype(),
        'monoisotopic_mass': pandas.Float64Dtype(),
        'ALogP': pandas.Float64Dtype(),
        'SLogP': pandas.Float64Dtype(),
        'XLogP': pandas.Float64Dtype(),
    })


def sdb_schema():
    return dask.dataframe.utils.make_meta({
        'compound': pandas.UInt64Index(),
        'identifier': pandas.StringDtype(),
        'identifier_type': pandas.StringDtype()
    })


def read_compound_db(path: str) -> dask.dataframe.DataFrame:
    return dask.dataframe.read_parquet(path)


def write_compound_db(ddf: dask.dataframe.DataFrame, path: str) -> None:
    pass