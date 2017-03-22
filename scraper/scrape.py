'''
Scrape.py is the main scraper.

It scrapes the S3 Bucket XML, parses it, and navigates
to each key. It attempts to download and pare the key
of each file, skipping the key when it fails.

It uses an port of the Python Image Library to process
binary data retrieved from the S3 bucket. It then uses
the local db module to store the metadata and EXIF data
of the image in the database.

Currently, it is tightly coupled to the waldo-recruting
S3 bucket, and could use a layer of abstraction around
image locations.
'''

#Standard library modules
import time
import xml.etree.ElementTree as ET
from io import BytesIO
from os.path import splitext

#Dependency modules
import requests
from PIL import Image, ExifTags

#Local modules
from db import ImageDatabase as ID

S3_DOCS = '{http://s3.amazonaws.com/doc/2006-03-01/}'
BUCKET_URL = 'http://s3.amazonaws.com/waldo-recruiting'

#Downloads the images from the S3 bucket
def run():
    #Setup database
    db = ID()
    db.setup()

    resp = requests.get(BUCKET_URL)
    bucket_result = ET.fromstring(resp.text)
    contents_elems = bucket_result.findall('%sContents' % S3_DOCS)
    for e in contents_elems:
        filename = e.find('%sKey' % S3_DOCS).text
        print('Inserting ', filename)
        url = "%s/%s" % (BUCKET_URL, filename)
        try:
            photo = Image.open(BytesIO(requests.get(url).content))
        except OSError as e:
            print(filename, ' failed to open. Skipping...')
            continue

        photo_id = db.insert_photo(
            url,
            filename,
            splitext(filename)[1],
            photo.height,
            photo.width
        )
        try:
            photo_exif = photo._getexif()
        except AttributeError as ae:
            print(filename, "has no exif data. Keeping image and skipping exif")
            continue
        for tag_no, value in photo_exif.items():
            try:
                tag_name = ExifTags.TAGS[tag_no]
            except KeyError as ke:
                print("Exif tag not recognized. Skipping...")
                continue
            
            #Bad values are currently being skipped. A future improvement
            #could handle bad values more gracefully by working with
            #database schema improvements to work with specific data
            #more directly.
            print("Adding", tag_name, "to photo", photo_id, "-", value)
            try:
                db.insert_exif(photo_id, tag_no, ExifTags.TAGS[tag_no], value)
            except ValueError as ve:
                print(tag_name, "had a bad value. Skipping...")
                continue
        print(filename, ' successfully inserted')
    time.sleep(999999999)

if __name__ == '__main__':
    run()
