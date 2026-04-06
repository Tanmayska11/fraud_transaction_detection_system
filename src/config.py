import os
from dotenv import load_dotenv

load_dotenv()

# Base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- DB CONFIG ---------------- #
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ---------------- PATHS ---------------- #
RAW_DATA_PATH = os.path.join(BASE_DIR, "data/raw/fraud_detection.csv")

MODEL_PATH = os.path.join(BASE_DIR, "models/trained/model.pkl")