import uvicorn

from core.api.api import patreon_pledge_checker

if __name__ == "__main__":
    uvicorn.run(patreon_pledge_checker, host="0.0.0.0", port=8000)