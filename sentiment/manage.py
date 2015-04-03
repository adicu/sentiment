from flask.ext.script import Manager
import os

from sentiment import app, db
app.config.from_object('config')

manager = Manager(app)

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

import imp

@manager.command
def migrate_db():
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	exec(old_model, tmp_module.__dict__)
	script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
	open(migration, "wt").write(script)
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('New migration saved as ' + migration)
	print('Current database version: ' + str(v))

if __name__ == '__main__':
    manager.run()