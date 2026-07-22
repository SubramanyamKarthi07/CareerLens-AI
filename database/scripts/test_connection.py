from sqlalchemy import text
from config.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))

        print("=" * 50)
        print("DATABASE CONNECTION SUCCESSFUL")
        print("=" * 50)

        print("Connected Database:", result.fetchone()[0])

except Exception as e:
    print("Connection Failed")
    print(e)