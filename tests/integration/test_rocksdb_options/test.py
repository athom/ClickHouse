# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long

import pytest

from helpers.client import QueryRuntimeException
from helpers.cluster import ClickHouseCluster

cluster = ClickHouseCluster(__file__)

node = cluster.add_instance('node', main_configs=['configs/rocksdb.yml'], stay_alive=True)


@pytest.fixture(scope='module', autouse=True)
def start_cluster():
    try:
        cluster.start()
        yield cluster
    finally:
        cluster.shutdown()

def test_valid_options():
    node.query("""
    CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
    DROP TABLE test;
    """)

def test_invalid_options():
    node.exec_in_container(['bash', '-c', "sed -i 's/max_background_jobs/no_such_option/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()
    with pytest.raises(QueryRuntimeException):
        node.query("""
        CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
        """)
    node.exec_in_container(['bash', '-c', "sed -i 's/no_such_option/max_background_jobs/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()

def test_table_valid_options():
    node.query("""
    CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
    DROP TABLE test;
    """)

def test_table_invalid_options():
    node.exec_in_container(['bash', '-c', "sed -i 's/max_open_files/no_such_table_option/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()
    with pytest.raises(QueryRuntimeException):
        node.query("""
        CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
        """)
    node.exec_in_container(['bash', '-c', "sed -i 's/no_such_table_option/max_open_files/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()

def test_valid_column_family_options():
    node.query("""
    CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
    DROP TABLE test;
    """)

def test_invalid_column_family_options():
    node.exec_in_container(['bash', '-c', "sed -i 's/num_levels/no_such_column_family_option/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()
    with pytest.raises(QueryRuntimeException):
        node.query("""
        CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
        """)
    node.exec_in_container(['bash', '-c', "sed -i 's/no_such_column_family_option/num_levels/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()

def test_table_valid_column_family_options():
    node.query("""
    CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
    DROP TABLE test;
    """)

def test_table_invalid_column_family_options():
    node.exec_in_container(['bash', '-c', "sed -i 's/max_bytes_for_level_base/no_such_table_column_family_option/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()
    with pytest.raises(QueryRuntimeException):
        node.query("""
        CREATE TABLE test (key UInt64, value String) Engine=EmbeddedRocksDB PRIMARY KEY(key);
        """)
    node.exec_in_container(['bash', '-c', "sed -i 's/no_such_table_column_family_option/max_bytes_for_level_base/' /etc/clickhouse-server/config.d/rocksdb.yml"])
    node.restart_clickhouse()
