import uvicorn
from server.settings import settings


def main() -> None:
    uvicorn.run(
        "server.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
    )


if __name__ == '__main__':
    main()
