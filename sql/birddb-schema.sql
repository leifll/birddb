--
-- The "config" table.
--
CREATE TABLE config (
  config_id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(500),
  description VARCHAR(2000),
  value VARCHAR(500)
);

ALTER TABLE config ADD PRIMARY KEY (config_id);

--
-- The "observation_type" table
--
CREATE TABLE observation_type (
  observation_type_id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(500)
);

ALTER TABLE observation_type ADD PRIMARY KEY (observation_type_id);

--
-- The "book" table.
--
CREATE TABLE book (
 book_id INT GENERATED ALWAYS AS IDENTITY,
 date DATE NOT NULL UNIQUE
);

ALTER TABLE book ADD PRIMARY KEY (book_id);

--
-- The "region" table.
--
CREATE TABLE region (
  region_id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(500) NOT NULL UNIQUE
);

ALTER TABLE region ADD PRIMARY KEY (region_id);

--
-- The "location" table.
--
CREATE TABLE location (
 location_id INT GENERATED ALWAYS AS IDENTITY,
 name VARCHAR(500) NOT NULL,
 region_id INT NOT NULL,
 UNIQUE(name, region_id)
);

ALTER TABLE location ADD PRIMARY KEY (location_id);
ALTER TABLE location ADD FOREIGN KEY (region_id) REFERENCES region;

--
-- The "photo" table.
CREATE TABLE photo (
 photo_id INT GENERATED ALWAYS AS IDENTITY,
 file_path VARCHAR(1000) UNIQUE,
 image_data BYTEA UNIQUE,
 time TIMESTAMP(0)
);

ALTER TABLE photo ADD PRIMARY KEY (photo_id);

--
-- The "printout" table.
--
CREATE TABLE printout (
 book_id INT NOT NULL,
 photo_id INT NOT NULL,
 page INT NOT NULL
);

ALTER TABLE printout ADD PRIMARY KEY (book_id,photo_id,page);
ALTER TABLE Printout ADD FOREIGN KEY (book_id) REFERENCES book;
ALTER TABLE Printout ADD FOREIGN KEY (photo_id) REFERENCES photo;

--
-- The "category" table.
--
CREATE TABLE category (
 category_id INT GENERATED ALWAYS AS IDENTITY,
 name VARCHAR(500) NOT NULL UNIQUE
);

ALTER TABLE category ADD PRIMARY KEY (category_id);

--
-- The "species" table.
--
CREATE TABLE species (
 species_id INT GENERATED ALWAYS AS IDENTITY,
 name VARCHAR(500) NOT NULL UNIQUE,
 category_id INT NOT NULL
);

ALTER TABLE species ADD PRIMARY KEY (species_id);
ALTER TABLE species ADD FOREIGN KEY (category_id) REFERENCES category;

--
-- The "observation" table.
--
CREATE TABLE observation (
 observation_id INT GENERATED ALWAYS AS IDENTITY,
 date DATE,
 location_id INT,
 species_id INT,
 photo_id INT,
 observation_type_id INT,
 "comment" VARCHAR(2000)
);

ALTER TABLE observation ADD PRIMARY KEY (observation_id);
ALTER TABLE observation ADD FOREIGN KEY (location_id) REFERENCES location;
ALTER TABLE observation ADD FOREIGN KEY (species_id) REFERENCES species;
ALTER TABLE observation ADD FOREIGN KEY (photo_id) REFERENCES photo ON DELETE SET NULL;
ALTER TABLE observation ADD FOREIGN KEY (observation_type_id) REFERENCES observation_type;
