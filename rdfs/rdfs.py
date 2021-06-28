import contextlib
import os
import subprocess
from typing import ContextManager, List, Tuple

import pyodbc

Graph = Tuple[str, str, str]


def rdfs_config(port: int, memory: int, workers: int):
    number_of_buffers = int((memory * 0.66) / 8000)
    max_dirty_buffers = int(3 * number_of_buffers / 4)

    with open('virtuoso.ini', 'w') as config:
        config.write('[Parameters]\n')
        config.write(f'ServerPort = {port}\n')
        config.write(f'NumberOfBuffers = {number_of_buffers}\n')
        config.write(f'MaxDirtyBuffers = {max_dirty_buffers}\n')
        config.write(f'ServerThreads = {workers}\n')
        config.write(f'ThreadsPerQuery = {workers}\n')
        config.write('DefaultIsolation = 2\n')
        config.write('ColumnStore = 1\n')


@contextlib.contextmanager
def rdfs_service(path: str) -> ContextManager[pyodbc.Connection]:
    proc = subprocess.Popen([path, '--foreground'], stderr=subprocess.PIPE)
    try:
        for line in iter(proc.stderr.readline, b''):
            if b'Server online at' in line:
                break
        if proc.poll() is not None:
            raise ChildProcessError('rdfs service unable to start')
        yield
    finally:
        proc.terminate()


@contextlib.contextmanager
def rdfs_connection(server: str, port: int, driver: str) -> ContextManager[pyodbc.Connection]:
    connection = pyodbc.connect(f'DRIVER={driver};HOST={server}:{port};UID=dba;PWD=dba')
    try:
        connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')

        yield connection
    finally:
        connection.close()


def rdfs_graph_prefix(prefix: str, graphs: List[Graph]) -> List[Graph]:
    return [(os.path.join(prefix, path), pattern, iri) for (path, pattern, iri) in graphs]


def rdfs_load(connection: pyodbc.Connection, graphs: List[Graph]) -> None:
    with connection.cursor() as cursor:
        cursor.executemany('ld_dir_all(?, ?, ?)', graphs)
    with connection.cursor() as cursor:
        cursor.execute('rdf_loader_run()')
