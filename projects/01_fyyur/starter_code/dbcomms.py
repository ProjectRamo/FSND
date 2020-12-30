# Had a lot of trouble running flask fb commands
# Basically none of the commands knew which db or app I was talking aobut
# found this script as an alternate suggestion in the Udacity forums
# posted by Mentor Mohamed S

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()

# python3 dbcomms.py db init
# python3 dbcomms.py db migrate
# python3 dbcomms.py db upgrade