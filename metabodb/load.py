from pandas import DataFrame
from typing import List


def load_sdf(file: str, keys: List[str]) -> DataFrame:
    from rdkit.Chem import PandasTools

    df = PandasTools.LoadSDF(file, molColName=None)
    return df[keys]
