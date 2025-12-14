import os
os.environ['TESTING']='true'

from app.database import SessionLocal, engine as db_engine, DATABASE_URL
print('DATABASE_URL:', DATABASE_URL)
print('Engine URL:', db_engine.url)
print('Original SessionLocal bind:', SessionLocal.kw.get('bind'))

from sqlalchemy import create_engine
TEST_ENGINE = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
print('TEST_ENGINE URL:', TEST_ENGINE.url)

SessionLocal.configure(bind=TEST_ENGINE, expire_on_commit=False)
print('After configure, SessionLocal bind:', SessionLocal.kw.get('bind'))

session = SessionLocal()
print('Session engine:', session.get_bind())
print('Session engine URL:', session.get_bind().url)
