import asyncio
from config import *

from app import create_app

def main():
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()