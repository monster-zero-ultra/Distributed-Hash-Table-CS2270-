### Distributed Hash Table (DHT) Implementation in Python 

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
 -  -  For testing, a dictonary is easiest  -  - 

## STRUCTURE 
1. Node Class
The Node class represents a node in the DHT. Each node has the following attributes:

id: A unique identifier for the node, generated using the SHA-1 hash function.
data: A dictionary that stores key-value pairs.
successor: A reference to the next node in the DHT ring.
predecessor: A reference to the previous node in the DHT ring.
finger_table: A list of references to other nodes in the DHT, used to quickly locate successors.

2. SQL_CONNECTOR Class
The SQL_CONNECTOR class manages the connection to a SQL Server database.
This class provides a connect() method that establishes the connection using SQLAlchemy.

3. DF_LOADER Class
The DF_LOADER class is responsible for loading data from a Pandas DataFrame into the DHT. It includes:

check_df(): Validates that the DataFrame has exactly two columns.
load_df_into_DHT(): Iterates over the DataFrame rows and inserts each key-value pair into the DHT.

4. sha1_hash Function
This function computes the SHA-1 hash of a given key and returns an integer representing the hashed value. It is used to generate node IDs and key IDs within the DHT.

5. DHT Operations
The following methods are key operations within the Node class:

 - join(): Allows a node to join the DHT by finding its successor and updating the DHT structure.
 - find_successor(): Finds the successor node for a given key ID.
 - closest_preceding_node(): Finds the closest preceding node to the given key ID using the finger table.
 - stabilize(): Ensures the DHT structure is correct by adjusting successor and predecessor pointers.
 - fix_fingers(): Updates the finger table for efficient lookups.
 - put(): Inserts a key-value pair into the DHT.
 - get(): Retrieves a value from the DHT based on the key.
 - 
6. Global Variables
 - M: Defines the size of the hash space (160 bits for SHA-1).
 - REPLICATION_FACTOR: Number of replicas for each piece of data to ensure fault tolerance.
   Features

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
   
project for CS2270, brain hurted, learned new stuff and things. C++. What more can i say... 10/10 good course would recommend
