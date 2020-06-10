import psycopg2
from crawl.spiders.config import config
 
def connectDbAndQuery(sql=""):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # set autocommit 
        conn.autocommit = True
 
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql)

        # set commit if not using autocommit
        #conn.commit()

        return cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
if __name__ == "__main__":
    print(connectDbAndQuery("SELECT version();"))