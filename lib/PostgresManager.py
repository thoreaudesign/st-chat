import copy
import psycopg2

# Database connection manager class. 
class PostgresManager:

    # "static" value represents config section for this class. 
    section = "Postgres"

    # "static" query strings. 
    INSERT_CHAT = '''INSERT INTO chat_log (timestamp, username, action, message) VALUES (%s, %s, %s, %s);'''

    # Takes ConfigurationManager cm as argument. 
    # Initializes Postgres config section and connects to database. 
    def __init__(self, cm):
        self.cm = copy.deepcopy(cm)
        self.set_config()
        self.connect()

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

    # Execute "INSERT_CHAT" query using args_list
    def insert_chat(self, args_list):
        try:
            self.check_connection() 
            self.cursor.execute(PostgresManager.INSERT_CHAT, args_list)
            self.conn.commit()
        except:
            raise

    # Check connection and handle retries. 
    def check_connection(self):
        if self.conn is None:
            print("No database connection... attempting to reconnect.")
            try:
                retries = self.config['retries']
                for i in range(1,retries):
                    print("Retry attempt {retry}...".format(retry=i))
                    self.conn = self.connect()
                    if self.conn is None:
                        print("Retry attempt {retry} failed...".format(retry=i))
                        continue
                    else:
                        print("Successfully reconnected!")
                        break;
                raise Exception("Lost database connection and attempted {n} retries... Failed to reconnect."
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
