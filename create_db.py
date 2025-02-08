from db_configuration import Base, engine
from models import *

# Create database tables
def create_tables():
    Base.metadata.create_all(engine)
