# exif-scraper
Grab photos from an S3 bucket and store their EXIF data in a database.

## Running with Docker Compose
The included `docker-compose.yml` will start a postgres service and run the image scraper. To run the scraper using docker compose, simply start the services from the repo's base directory:

    [sudo] docker-compose up

Once the scraper starts inserting data into the database, get the id of the postgres container:

    [sudo] docker ps

And then use that ID to connect to the postgres container and query the database:

    [sudo] docker exec -it <container_id> psql postgres postgres

## Running in other python 3 environments
To run in other python 3 environments, you will have to edit `scraper/db.py` to connect to a Postgresql installation. Then, cd to `scraper` and run `scrape.py`:

    python scrape.py

Note that the script will run (basically) forever if you do not manually stop it. This is so users working with Docker Compose can inspect the database at their leisure.

## Additions

This project will benefit from a number of additions. Each code file has extensive comments describing how it can be improved. Below is a list of other additions that can improve the project as a whole.

### Image Source Agnostic
At present, the scraper has only been tested against one input: the Waldo Recruiting S3 bucket. The scraper would be greatly improved if it could accept many other types of inputs: an image URL, a webpage URL that contains many images, a local directory that contains images, an RSS feed with images, an Instagram account, a zip file containing images.

This could be achieved by creating an `ImageSource` abstract class and using an argument parser to implement a factory method. The factory method would analyze the image source argument, provided by the user in the command line, and instantiate the appropriate ImageSource ancestor.

### Image Storage
Currently, images are retrieved and their binary data is read into memory. Once the EXIF data is stored, the image data is lost. This project would benefit with a means to store images in an easily retrievable location after images have been downloaded. A new module named something like `ImageStore` would implement the web request logic and return a set of images. When an image is requested, the ImageStore module would check to see if it has downloaded that image recently. If it has, it would retrieve it from the local disk. If it hasn't, then it will download the image, store it locally, and return the appropriate data.

Subclasses of `ImageStore` could be designed to store images in S3 buckets, Dropbox, Google Drive, or social media accounts.

### GUI
Once the source of images is agnostic and image storage is working, the project could greatly benefit from an interface to view the images and their EXIF data, and perhaps also keep track of storage locations and images sources that have been previously scraped. If I continued down this path, I would adapt the existing python code to a Django web application, probably using the Django Admin panel to get a feel for working with the data, and then building a more customized UI.

### Performance improvements

The following is a short list of general performance improvements. Code files also contain more specific performance improvements.

#### Concurrency
The process of downloading an image and storing its data in the database could certainly be multi-threaded. Using a tool like [Celery](http://www.celeryproject.org/) we could offload the image-by-image code to separate threads. We would have to do some re-organization of the database code to account for possible race conditions, especially with the auto-incrementing primary key on the images table. Once race conditions are accounted for, the entire process would run much more quickly, especially on processors where eight or sixteen threads could execute at once.

#### Caching
As stated previously, we could add an ImageStore module that would save images to the local hard disk or other locations, eliminating the need to download them again. We could take this caching behavior one step further by linking image URLs to a JSON string in a caching server. So, in instances where users are working with many different data sources, some of which contain the same image URL many times, the EXIF data could be retrieved as a JSON string from the cache server, without ever having to download the URL or open the binary file in memory.
