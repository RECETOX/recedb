from sqlalchemy import MetaData, Table, Column, ForeignKey, BigInteger, String, Float


def schema():
    meta = MetaData()
    Table('pathways', meta,
          Column('pathway', BigInteger, primary_key=True))
    Table('compounds', meta,
          Column('compound', BigInteger, primary_key=True),
          Column('iupac_inchi', String),
          Column('iupac_inchikey', String(27)),
          Column('iupac_systematic_name', String),
          Column('iupac_traditional_name', String),
          Column('complete_smiles', String),
          Column('qsar-ready_smiles', String),
          Column('ms-ready_smiles', String),
          Column('monoisotopic_mass', Float(64)))
    Table('pathway_associations', meta,
          Column('pathway', ForeignKey('pathways.pathway')),
          Column('compound', ForeignKey('compounds.compound')))
    Table('standard_atomic_weights', meta,
          Column('isotope', String(5), primary_key=True),
          Column('mass', Float(64)),
          Column('abudance', Float(64)))
    return meta
