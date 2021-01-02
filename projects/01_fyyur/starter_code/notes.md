Created a database called fyyurdb using the interface.
Not sure if the migrations are powerful enough to completely create a new database.

- Created helper_files folder with helper files

password is postgrespass

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

python3 dbcomms.py init
python3 dbcomms.py migrate
python3 dbcomms.py upgrade

- Since the Udacity code produces mixed case table names, you have to use "" in postgres
- Had to add a password to get the database to work
- After database migrations, Artist and Venue were added

Todo: read Json data in
