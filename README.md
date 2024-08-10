Distributed Hash Table (DHT) Implementation in Python

This project implements a Distributed Hash Table (DHT) using the Chord protocol with SHA-1 hashing. The DHT can store key-value pairs and distribute them across multiple nodes. It also includes functionality for loading data from different sources (e.g., Pandas DataFrames, SQL databases, and dictionaries).

### Prerequisite python packages
- `pandas`
- `sqlalchemy`
- `pyodbc` (if you're connecting to a SQL Server database)

### For SQL dataset connection
 - server: SQL server address
 - port: Port number for the SQL server
 - user: Username for SQL server access
 - password: Password for the SQL server
 - database: Name of the database to connect to

#### LOADING DATA ###
In main() function, replace test_data with your data source of choice.
The script supports loading data from three sources:

Pandas DataFrame: Provide a DataFrame with two columns (key and value). The columns do not need to be named 'key' and 'value'.
SQL Database: Provide a list containing the SQL connection details and the table name to load data from a SQL table.
Dictionary: Provide a Python dictionary where keys represent the data keys and values represent the data values.

### Flow (from progressive) 
 - Script initializes the DHT and checks if it's empty.
 - If the DHT is empty, it creates an initial node.
 - It then loads the data into the DHT based on the source type (DataFrame, SQL, or dictionary ((or tells you to try again)))
 - While loading, script will periodically stabalize, fix finger tables, and check nodes to maintain the DHT
 - The script prints the stored data in the DHT.

 - 
### Current Features 
 - Distributed Hash Table (DHT): A basic implementation of DHT using the Chord protocol.
   
 - SHA-1 Hashing: Secure hashing of keys using the SHA-1 algorithm.
   
 - Data Replication: Data is replicated across multiple nodes for fault tolerance.
   
 - Finger Tables: Nodes maintain a finger table to efficiently find the successor for a given key.
   
 - Data Loading: Supports loading data from Pandas DataFrames, SQL databases, and dictionaries.

### Next Steps
 -  Leave function
    To allow for a node to leave the DHT and notify all other nodes to reorganize data if needed to maintin redundancy and/or stability
 - Multiple user support
   Needing working threading to support conflicts if more than one person is on
   functinality of some sort of online sharing of the table
   
