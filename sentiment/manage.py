from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from sentiment import app, db
app.config.from_object('config')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from migrate.versioning import api
from config.config import SQLALCHEMY_DATABASE_URI
from config.config import SQLALCHEMY_MIGRATE_REPO
import os.path

@manager.command
def create_db():
    db.create_all()

    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

if __name__ == '__main__':
    manager.run()