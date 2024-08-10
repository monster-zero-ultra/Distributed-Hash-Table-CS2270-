import hashlib
import threading
import time
import pandas as pd
from sqlalchemy import create_engine



# server = 'localhost'
# port = '1433' 
# USER = '********'
# PASSWORD = '********'
# DATABASE = '********'


# table_name = '[NHS PANDAS SQL DATASET]'
# query = f'SELECT * FROM {table_name}'

# NHS_df = pd.read_sql(query, engine)

M = 160  # Size of the hash space (SHA-1 produces 160-bit hashes)
REPLICATION_FACTOR = 3


class SQL_CONNECTOR:
    def __init__(self, server, port, user, password, database):
        self.server = server
        self.port = port 
        self.USER = user
        self.PASSWORD = password
        self.DATABASE = database
    def connect(self):
        if(not self.server or not self.port or not self.USER or not self.PASSWORD or not self.DATABASE):
            raise ValueError('Please provide all the required information for SQL server access')
        engine = create_engine(f'mssql+pyodbc://{self.USER}:{self.PASSWORD}@{self.server}:{self.port}/{self.DATABASE}?driver=ODBC+Driver+17+for+SQL+Server')
        return engine

class DF_LOADER:
    def check_df(self, df):
        if(not isinstance(df, pd.DataFrame)):
            raise ValueError('Please provide a pandas dataframe')
        if len(df.columns) != 2:
            raise ValueError("""Please provide a dataframe with only 2 columns, 
                             the first being the key and the second being the value
                             the columns do not need be named 'key' and 'value'""")
        return True
    def load_df_into_DHT(self, df, node):
        if(self.check_df(df)):
            for index, row in df.iterrows():
                key = row[0]
                value = row[1]
                node.put(key, value)
        return True

def sha1_hash(key):
    return int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16)

class Node:
    dht_status = {
        'is_empty': True,
        'existing_node' :None
    }
    # Constructor
    def __init__(self, node_id):
        self.id = node_id
        self.data = {}
        self.successor = self
        self.predecessor = self
        self.finger_table = [self] * M
        self.lock = threading.Lock()


    def join(self, existing_node):
        #print("Join method called")
        if existing_node:
            self.successor = existing_node.find_successor(self.id)
            self.predecessor = None
            print("Successor found:", self.successor.id)
        else:
           
            self.successor = self
            self.predecessor = self
        print("Stabilizing...")
        self.stabilize()
        print("Fixing fingers...")
        self.fix_fingers()
        print("Replicating data to successor...")
        self.replicate_data_to_successor()
        Node.dht_status["is_empty"] = False
        Node.dht_status["existing_node"] = self
        print("Join method completed")

    def find_successor(self, key_id):
        # If the DHT has only one node or if this node is the correct successor
        if self.id == self.successor.id or (key_id > self.id and key_id <= self.successor.id):
            return self.successor
        else:
            node = self.closest_preceding_node(key_id)
            
            # Avoid infinite recursion by adding a base case
            if node.id == self.id:  # If closest preceding node is itself, return self as a fallback
                return self
            
            return node.find_successor(key_id)

    def closest_preceding_node(self, key_id):
        for i in range(M-1, -1, -1):
            if self.finger_table[i].id > self.id and self.finger_table[i].id < key_id:
                return self.finger_table[i]
        return self

    def stabilize(self):
        
            x = self.successor.predecessor
            if x and self.id < x.id < self.successor.id:
                self.successor = x
            self.successor.notify(self)

    def notify(self, node):
        
            if not self.predecessor or (self.predecessor.id < node.id < self.id):
                self.predecessor = node

    def fix_fingers(self):
        
            for i in range(M):
                start = (self.id + 2**i) % 2**M
                self.finger_table[i] = self.find_successor(start)

    def check_predecessor(self):
        
            if self.predecessor and self.predecessor == self:
                self.predecessor = None

    def put(self, key, value):
        key_id = sha1_hash(key)
        node = self.find_successor(key_id)
        with node.lock:
            node.data[key_id] = value
            #print(f"Node {node.id}: {key} => {value}")

    def get(self, key):
        key_id = sha1_hash(key)
        node = self.find_successor(key_id)
        with node.lock:
            return node.data.get(key_id, "NOT FOUND")
        
    def store_data(self, key_id, value):
        
            self.data[key_id] = value

    def retrieve_data(self, key_id):
        
            return self.data.get(key_id, "NOT FOUND")

    def replicate_data(self, primary_node, key_id, value):
        node = primary_node
        for _ in range(REPLICATION_FACTOR - 1):
            node = node.successor
            node.store_data(key_id, value)

    def replicate_data_to_successor(self):
        
            for key_id, value in self.data.items():
                self.successor.store_data(key_id, value)

        

    def print_data(self):
        
            for key, value in self.data.items():
                print(f"Node {self.id}: {key} => {value}")

def stabilize_network(node):
    while True:
        node.stabilize()
        node.fix_fingers()
        node.check_predecessor()
        time.sleep(5)


def main():
    #load data
    print("""Load you data in main function 
          if your data is a pandas dataframe please input the dataframe in the ""Data_to_be_loaded"" variable, 
          if your data is a sql table, please input a list of the following:
          (server, port, user, password, database, table_name),
          for any data that is not a pandas dataframe or sql table, please input the data itself in a dictonary format""")
    

########## Load your data here ##########
    
    Data_to_be_loaded = test_data

####### delete test_data and replace ####
##### for all data types besides sql ####

#########################################


    data_type = type(Data_to_be_loaded)
   # print(test_data)

    if data_type == pd.DataFrame:
        df = Data_to_be_loaded
        df_loader = DF_LOADER()
        if(Node.dht_status['is_empty']):
            node = Node(sha1_hash("initial_node"))
            node.join(None)
            Node.dht_status['existing_node'] = node
            Node.dht_status['is_empty'] = False
            df_loader.load_df_into_DHT(df, node)
        else:
            df_loader.load_df_into_DHT(df, Node.dht_status['existing_node'])

    elif data_type == list and len(Data_to_be_loaded) == 6:
        server, port, user, password, database = Data_to_be_loaded
        table_name = Data_to_be_loaded[-1]
        sql_connector = SQL_CONNECTOR(server, port, user, password, database)
        engine = sql_connector.connect()
        query = f'SELECT * FROM [{table_name}]'
        NHS_df = pd.read_sql(query, engine)
        df_loader = DF_LOADER()
        if(Node.dht_status['is_empty']):
            node = Node(sha1_hash("initial_node"))
            node.join(None)
            Node.dht_status['existing_node'] = node
            Node.dht_status['is_empty'] = False
            df_loader.load_df_into_DHT(NHS_df, node)
        else:
            df_loader.load_df_into_DHT(NHS_df, Node.dht_status['existing_node'])


    elif data_type == dict:
        print("Loading dictionary data into DHT...")
        if Node.dht_status['is_empty']:
            print("DHT is empty, creating initial node...")
            node = Node(sha1_hash("initial_node"))
            node.join(None)
            Node.dht_status['existing_node'] = node
            Node.dht_status['is_empty'] = False
            print("Initial node created")
        else:
            node = Node.dht_status['existing_node']
        for key, value in Data_to_be_loaded.items():
            print(f"Inserting {key}: {value}")
            node.put(key, value)
        node.print_data()
    else:
        raise ValueError('Please provide a valid data type')

    print("Main function completed")

if __name__ == "__main__":
    main()