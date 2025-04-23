import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://inventory_manager_s9lo_user:ih2D3zpTmmYmypQu9p1PjBBz4QtvDhwR@dpg-d04chqp5pdvs73c81l2g-a/inventory_manager_s9lo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
