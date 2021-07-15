import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import create_app, db

config_name = os.environ.get("FLASK_ENV")
app = create_app(config_name)

# migrations
Migrate(app, db)
from models import models
# end of migrations


if __name__ == "__main__":
    app.run()