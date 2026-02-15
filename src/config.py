import os

class Config:
    DEBUG = False 
    DB_NAME = "data/gym_debug.db" if DEBUG else "data/gimnasio.db"
    # DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)
    APP_NAME = "Gestión Gym (Dev)" if DEBUG else "Gimnasio Pro"