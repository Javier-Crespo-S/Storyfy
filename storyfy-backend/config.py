class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///storyfy.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-key"