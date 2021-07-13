import psycopg2
import yaml
import os


def connect():
    config = {}
    yml_path = os.path.join(os.path.dirname(__file__), '../config/db.yml')
    with open(yml_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return psycopg2.connect(dbname=config['database'],
                            user=config['user'],
                            password=config['password'],
                            host=config['host'],
                            port=config['port'])


def test():
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT VERSION()')
    print(cur.fetchone()[0].startswith('PostgreSQL'))
    conn.close()


test()

