from typing import List

import pandas
from openbabel.openbabel import OBConversion, OBMol


def read_inchi(inchi: List[str]) -> List[OBMol]:
    conv = OBConversion()
    molecules = [OBMol()] * len(inchi)
    assert conv.SetInFormat('inchi')
    assert all(conv.ReadString(mol, val) for mol, val in zip(molecules, inchi))
    return molecules


def compute_inchi(molecules: List[OBMol]) -> List[str]:
    conv = OBConversion()
    assert conv.SetOutFormat('inchi')
    return [conv.WriteString(mol) for mol in molecules]


def compute_inchikey(molecules: List[OBMol]) -> List[str]:
    conv = OBConversion()
    assert conv.SetOutFormat('inchikey')
    return [conv.WriteString(mol) for mol in molecules]


def compute_canonical_smiles(molecules: List[OBMol]) -> List[str]:
    conv = OBConversion()
    assert conv.SetOutFormat('can')
    return [conv.WriteString(mol) for mol in molecules]


def compute_molecular_formula(molecules: List[OBMol]) -> List[str]:
    return [mol.GetFormula() for mol in molecules]


def compute_monoisotopic_mass(molecules: List[OBMol]) -> List[float]:
    return [mol.GetMolWt() for mol in molecules]


def remove_salts_and_fragments(molecules: List[OBMol]) -> List[OBMol]:
    for mol in molecules:
        if mol.NumHvyAtoms() > 5:
            mol.StripSalts(0)
            mol.DeleteData(mol.GetData('inchi')) # wipe InChI cache
    return molecules


def remove_organometallics_and_anorganics(molecules: List[OBMol]) -> List[OBMol]:
    pass


def compute_qsar_ready_smiles(molecules: List[OBMol]) -> List[str]:
    conv = OBConversion()
    conv.SetOutFormat('inchi')
    conv.AddOption('noiso', conv.OUTOPTIONS)
    conv.AddOption('nochg', conv.OUTOPTIONS)
    conv.AddOption('nostereo', conv.OUTOPTIONS)

    conv = OBConversion()
    conv.SetOutFormat('can')




def cdb_compute(df: pandas.DataFrame):
    molecules = read_inchi(df.iupac_inchi)

    return {
        'iupac_inchi': compute_inchi(molecules),
        'iupac_inchikey': compute_inchikey(molecules),
        'canonical_smiles': compute_canonical_smiles(molecules),
        'molecular_formula': compute_molecular_formula(molecules),
        'monoisotopic_mass': compute_monoisotopic_mass(molecules),
    }
