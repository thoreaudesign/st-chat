import copy
import psycopg2

class PostgresManager:

    section = "Postgres"

    INSERT_CHAT = '''INSERT INTO chat_log (timestamp, username, action, message) VALUES (%s, %s, %s, %s);'''

    def __init__(self, cm):
        self.cm = copy.deepcopy(cm)
        self.set_config()
        self.connect()

    def set_config(self):
        if PostgresManager.section in self.cm.parser.sections():
            self.config = self.cm.parser[PostgresManager.section]
        else:
            raise Exception("Invalid configuration file at {config_path}. Missing section '{section}.'"
                .format(config_path=self.cm.parser.path, section=PostgresManager.section))

    def connect(self):
        try:
            self.conn = psycopg2.connect(host=self.config['host'], database=self.config['name'], 
                        port=self.config['port'], user=self.config['user'],password=self.config['pass'])
            self.cursor = self.conn.cursor()

        except Exception:
            raise

    def insert_chat(self, args_list):
        try:
            self.check_connection() 
            self.cursor.execute(PostgresManager.INSERT_CHAT, args_list)
            self.conn.commit()
        except:
            raise

    def check_connection(self):
        if self.conn is None:
            try:
                retries = self.config['retries']
                for i in range(1,retries):
                    self.conn = self.connect()
                    if self.conn is None:
                        continue
                    else:
                        break;
                raise Exception("Lost database connection and attempted {n} retries... Failed to reconnect."
                    .format(n=retries))
            except:
                raise

    def __del__(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except AttributeError:
            return
