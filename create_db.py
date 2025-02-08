from db_configuration import Base, engine
from models import *

# Create database tables
Base.metadata.create_all(engine)
