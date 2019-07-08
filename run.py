
from pychall import *


if __name__ == "__main__":
    psql.drop_dbs(dbnames=['places','people'])
    psql.create_dbs(dbnames=['places','people'])
    places.psql.createtbl()
    places.psql.insert_json()
    people.psql.createtbl()
    people.psql.insert_json()
