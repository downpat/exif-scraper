'''
ImageDatabase

This is a very simple interface to the image database.

It is specifically designed for inserting photo metadata
and EXIF data.

This class could be redesigned as an abstract class, and
subclasses could be designed for working with different
kinds of databases.

At the moment, it does no cleanup, so it could benefit from
a close() method to clean up the database connection.

'''

import psycopg2 as ps

class ImageDatabase:

    def __init__(self):
        '''
        Constructor

        Connects to the postgres database in the postgres docker
        container described in docker-compose.yml.

        This could benefit
        from arguments that take the DB connection parameters, or read
        connection parameters in from a config file.
        '''
        self.conn = ps.connect(
            dbname='postgres',
            user='postgres',
            host='db'
        )
        self.curs = self.conn.cursor()

    def setup(self):
        '''
        Sets up the database tables.

        Right now, it drops every table whenever its run. It could
        probably benefit from a boolean argument that determines
        whether to drop a table if it exists or skip the creation.
        tables.sql would need to be updated to faciliate such a
        change.
        '''
        self.curs.execute(open('tables.sql', 'r').read())

    def insert_photo(self, origin_url, filename, extension, height, width):
        '''
        Inserts photo metadata into the database.

        This is straightforward and useful for the specific purposes of
        the project. It's convenient, but also tightly coupled to the
        image data source and this database schema.
        '''
        self.curs.execute('''
            INSERT INTO images (origin_url, filename, extension, height, width)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (origin_url, filename, extension, height, width))
        self.conn.commit()
        return self.curs.fetchone()[0]

    def insert_exif(self, image_id, tag_no, tag_name, value):
        '''
        Inserts photo EXIF data into the database

        The main problem with this method is that it coerces the 'value'
        argument to a string. Sometimes value is a primitive, sometimes
        it's a collection. Our data would be easier to work with a different
        database schema. tables.sql has more thoughts on that.
        '''
        self.curs.execute('''
            INSERT INTO images_exif (image_id, tag_no, tag_name, value)
            VALUES (%s, %s, %s, %s)           
        ''', (image_id, tag_no, tag_name, str(value)))
        self.conn.commit()

if __name__ == '__main__':
    ImageDatabase().setup()
