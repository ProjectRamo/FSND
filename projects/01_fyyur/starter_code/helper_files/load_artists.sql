
INSERT INTO "Artist"(id,name,genres,city,state,phone,website,facebook_link,seeking_venue,seeking_description,image_link)
VALUES (11,'Guns N Petals','{"Rock n Roll"}','San Francisco','CA','326-123-5000','https://www.gunsnpetalsband.com','https://www.facebook.com/GunsNPetals','True','Looking for shows to perform at in the San Francisco Bay Area!','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
 )
RETURNING *;

INSERT INTO "Artist"(id,name,genres,city,state,phone,website,facebook_link,seeking_venue,seeking_description,image_link)
VALUES (12,'Matt Quevedo','{Jazz}','New York','NY','300-400-5000','','https://www.facebook.com/mattquevedo923251523','False','','https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
 )
RETURNING *;

INSERT INTO "Artist"(id,name,genres,city,state,phone,website,facebook_link,seeking_venue,seeking_description,image_link)
VALUES (13,'The Wild Sax Band','{Jazz,Classical}','San Francisco','CA','432-325-5432','','','False','','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
 )
RETURNING *;