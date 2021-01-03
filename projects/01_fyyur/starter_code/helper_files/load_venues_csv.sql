COPY "Venue"(id, name, genres, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link)
FROM 'helper_files/data_venues.csv'
DELIMITER ','
CSV HEADER;