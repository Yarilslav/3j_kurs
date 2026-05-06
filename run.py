import uvicorn
from app.core.config import settings

# Локальна точка запуску. У production reload вимикається через APP_RELOAD=false.
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.app_port,
        reload=settings.APP_RELOAD,
    )
