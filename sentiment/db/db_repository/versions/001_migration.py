from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
days = Table('days', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime, nullable=False),
    Column('sentiment', Float, nullable=False),
    Column('comment1', String, nullable=False),
    Column('comment1_url', String, nullable=False),
    Column('comment2', String, nullable=False),
    Column('comment2_url', String, nullable=False),
    Column('comment3', String, nullable=False),
    Column('comment3_url', String, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['days'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['days'].drop()
