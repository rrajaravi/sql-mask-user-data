#!/usr/bin/env python
import time

from sqlalchemy import create_engine
import click


USER_TABLE_NAME = 'user'
EMAIL_FIELD_NAME = 'email'
PASSWORD_FIELD_NAME = 'password'


def execute_db_query(connection, query):
    print("Processing query: {}".format(query))
    result = connection.execute(query)


@click.command()
@click.option('--db-name', required=True)
@click.option('--db-host', required=True)
@click.option('--db-user', required=True)
@click.option('--db-password', required=True)
@click.option('--new-email-suffix', required=True)
@click.option('--new-password-hash', required=True)
def main(db_name: str, db_host: str, db_user: str, db_password: str, new_email_suffix: str, new_password_hash: str):
    database_url = 'mysql://{}:{}@{}:3306/{}'.format(
        db_user, db_password, db_host, db_name)
    password_update_q = 'UPDATE {} SET {}="{}";'.format(
        USER_TABLE_NAME, PASSWORD_FIELD_NAME, new_password_hash)
    email_update_q = "UPDATE {} SET {}=CONCAT_WS(id, {})".format(
        USER_TABLE_NAME, EMAIL_FIELD_NAME, new_email_suffix)
    start = time.time()
    print('Start time: {}'.format(start))

    # db engine and connection
    engine = create_engine(database_url)
    connection = engine.connect()

    # update begins
    # password update
    execute_db_query(connection, password_update_q)

    # email update
    execute_db_query(connection, email_update_q)

    # Close db connection
    connection.close()
    print('Time elapsed: {}s'.format(time.time() - start))


if __name__ == "__main__":
    main()
