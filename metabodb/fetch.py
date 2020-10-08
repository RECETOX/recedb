from typing import Dict

import sqlalchemy

from metabodb.load import load_sdf
from metabodb.schema import schema


def fetch(args):
    engine = sqlalchemy.create_engine(f'sqlite:///{args.dst}')
    schema().create_all(engine)

    mapping = get_mapping('pubchem')

    for source in args.src:
        print(f'fetching {source}...')

        df = load_sdf(file=source, keys=list(mapping.values()))
        df.rename(columns=mapping, inplace=True)
        df.to_sql('compounds', con=engine, index=False, if_exists='append')


def get_mapping(database: str) -> Dict[str, str]:
    return {
        'pubchem': {
            'iupac_inchi': 'PUBCHEM_IUPAC_INCHI',
            'iupac_inchikey': 'PUBCHEM_IUPAC_INCHIKEY',
            'iupac_systematic_name': 'PUBCHEM_IUPAC_SYSTEMATIC_NAME',
            'iupac_traditional_name': 'PUBCHEM_IUPAC_TRADITIONAL_NAME',
        }
    }[database]
