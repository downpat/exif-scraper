#Standard library modules
import xml.etree.ElementTree as ET

#Dependency modules
import requests

S3_DOCS = '{http://s3.amazonaws.com/doc/2006-03-01/}'
BUCKET_URL = 'http://s3.amazonaws.com/waldo-recruiting'

#Downloads the images from the S3 bucket
def run():
    resp = requests.get(BUCKET_URL)
    bucket_result = ET.fromstring(resp.text)
    contents_elems = bucket_result.findall('%sContents' % S3_DOCS)
    for e in contents_elems:
        filename = e.find('%sKey' % S3_DOCS).text
        print("%s/%s" % (BUCKET_URL, filename))
    

if __name__ == '__main__':
    run()
