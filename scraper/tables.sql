/*
 * This is a barebones schema designed to do nothing
 * more than the task at hand. The database schema does
 * not reflect any particular problem domain, and so is
 * does not really treat any data as more important. Height
 * and Weight are used as examples of metadata that could be
 * stored directly in an image row, but EXIF data could
 * be efficiently stored this way too, depending on
 * the importance of a specific tag.
 *
 * Suggested Improvements:
 *  - Add highly-used EXIF tags as columns to the images table. This would
 *     eliminate the need for unnecessary table joins in queries.
 *  - Create more tables for EXIF tags that are closely related. That way
 *     instead of complicated key-value store queries for images_exif, simple
 *     joins with the images table make navigating data straightforward.
 */

DROP TABLE IF EXISTS images CASCADE;
CREATE TABLE images (
	id SERIAL PRIMARY KEY,
	origin_url text,
	filename text,
	extension text,
	height integer,
	width integer
);

DROP TABLE IF EXISTS images_exif;
CREATE TABLE images_exif (
	image_id integer REFERENCES images,
	tag_no integer,
	tag_name text,
	value text,
	PRIMARY KEY(image_id, tag_no)
);
