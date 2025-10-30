import os

import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run("app:app", host=host, port=port, reload=True if os.getenv("ENV") == "development" else False)
