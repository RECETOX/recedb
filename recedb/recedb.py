from typing import List

import click
import dask.bag
import dask.dataframe

from recedb.compute import cdb_compute
from recedb.schema import cdb_schema


@click.group()
def cli():
    pass


@cli.command()
@click.argument('dst', type=click.Path())
@click.option('-i', '--inchi', type=click.Path(exists=True), multiple=True)
def create(dst: str, inchi: List[str]) -> None:
    """
    Generate recetox database
    """
    seed = dask.bag.read_text(inchi)
    seed = seed.distinct()
    seed = seed.repartition(partition_size='5MB')

    ddf = seed.to_dataframe({'iupac_inchi': 'string'})
    ddf = ddf.map_partitions(cdb_compute, meta=cdb_schema())

    ddf.to_parquet(dst)


@cli.command()
@click.argument('src', type=click.Path(exists=True), nargs=-1)
@click.argument('dst', type=click.Path())
def merge(src: List[str], dst: str) -> None:
    """
    Merges multiple recetox databases into one
    """
    pass


if __name__ == '__main__':
    cli()
