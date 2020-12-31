import copy
import psycopg2

# Database connection manager class. 
class PostgresManager(object):

    # "static" value represents config section for this class. 
    section = "Postgres"

    # "static" query strings. 
    INSERT_CHAT = '''INSERT INTO chat_log (timestamp, username, action, message) VALUES (%s, %s, %s, %s);'''
    INSERT_EVENT = '''INSERT INTO sport_event (timestamp, sport, match_title, data_event) VALUES (%s, %s, %s, %s);'''
    INSERT_EXECUTION = '''INSERT INTO execution (timestamp, symbol, market, price, quantity, executionEpoch, stateSymbol) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
  
    # Takes ConfigurationManager cm as argument. 
    # Initializes Postgres config section and connects to database. 
    def __init__(self, cm):
        self.cm = copy.deepcopy(cm)
        self.conn = None
        self.cursor = None
        self.set_config()
        self.check_connection()

    # Get [Postgres] section from config.ini and set as self.config. 
    def set_config(self):
        if PostgresManager.section in self.cm.parser.sections():
            self.config = self.cm.parser[PostgresManager.section]
        else:
            raise Exception("Invalid configuration file at {config_path}. Missing section '{section}.'"
                .format(config_path=self.cm.parser.path, section=PostgresManager.section))

    # Connect to database using config values. Set cursor for executing Postgres queries. 
    def connect(self):
        try:
            self.conn = psycopg2.connect(host=self.config['host'], database=self.config['name'], 
                        port=self.config['port'], user=self.config['user'],password=self.config['pass'])
            self.cursor = self.conn.cursor()

        except Exception:
            raise

    # Execute query using args_list
    def insert(self, query, args_list):
        try:
            self.cursor.execute(query, args_list)
            self.conn.commit()
        except:
            self.check_connection()
            raise

    # Check connection and handle retries. 
    def check_connection(self):
        if self.conn is None or self.cursor is None:
            print("No database connection... attempting to connect.")
            try:
                retries = self.config['retries']
                for i in range(0,int(retries)):
                    display_retry = i+1
                    try:
                        self.connect()
                        print("Successfully connected!")
                        return
                    except: 
                        print("Retry attempt {retry} failed...".format(retry=display_retry))
                        continue
                raise Exception("Failed to reconnect."
                    .format(n=retries))
            except:
                raise

    # Disconnect from database when class is destroyed. 
    def __del__(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except AttributeError:
            return
