import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(tags=["core"])


@router.get("/health")
def health():
    status = {"status": "ok", "db": "connected"}
    logger.info("Health check successful", extra=status)
    return status


# later, after postgres is set up, we can implement a real check here
# @router.get("/health")
# def health(db: Session = Depends(get_db)):
#     try:
#         db.execute(text("SELECT 1"))
#         db_status = "ok"
#     except Exception:
#         db_status = "down"

#     return {"status": "ok", "db": db_status}
