USER = 'postgres'
PASSWORD = 'Manuchehr1313'
HOST = 'localhost'
PORT = 5432
DB_NAME = 'story'

CONNECTION_ARGS = {
	"user": USER,
	"password": PASSWORD,
	"host": HOST,
	"port": PORT,
	"database": DB_NAME
}

CONNECTION_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
