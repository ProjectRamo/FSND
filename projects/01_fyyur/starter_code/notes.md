
## database notes

Created a database called fyyurdb using the interface.
Not sure if the migrations are powerful enough to completely create a new database.

- Created helper_files folder with helper files


password is postgrespass
fyyurdb=# ALTER USER postgres PASSWORD 'postgrespass';

Had to create the database manually but not the tables.

- Since postgres is a different unix user, one has to do the following to get to the right directory inside the psql prompt:
\!
navigate to the right directory
exit
\cd ../../../home/oh/code/ud-fullstack/FSND/projects/01_fyyur/starter_code
- then run the program
\i helper_files/test.sql

Ran all three migrate steps using the helper python file dbcomms.py (for database communications)
(It has to be in the 01_fyyur folder to work so move it there before running)

python3 dbcomms.py db init
python3 dbcomms.py db migrate
python3 dbcomms.py db upgrade

and if you push and pull from git betweeen multiple computers, you will need:
python3 dbcomms.py db stamp 

- Since the Udacity code produces mixed case table names, you have to use "" in postgres
- Had to add a password to get the database to work
- After database migrations, Artist and Venue were added

## Reading in the data

This was painful. Originally tried to read it in as JSON.
Used load_venues.sql to read load in the JSON.
Problem: SQL Alchemy wanted it as Boolean but SQL wanted it passed as text and then cast.

Tried to load in the CSV directly by converting JSON-> CSV.
data_venues.csv is the csv and the SQL command was simply:
  \copy "Venue" from helper_files/data_venues.csv with csv header;

However this was not easy because it doesn't read the header for cues as to what the columns are. It was easier to read the columns in again and migrate them in the right order. This did require a drop table.

\copy "Artist" from helper_files/artist_mod.csv with csv header;

and finally the shows were added manually to try and link them up with each artist and venue

For loading in the shows, wrote up some PSQL by hand in load_shows.sql and copy and pasted them into psql as postgres

