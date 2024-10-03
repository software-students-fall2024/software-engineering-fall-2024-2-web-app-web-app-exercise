from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
print(f"SECRET_KEY: {secret_key}")