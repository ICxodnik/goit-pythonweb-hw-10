from fastapi import APIRouter, Depends, Request, UploadFile, File
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import User
from src.services.auth import get_current_user
from limiter import limiter
from src.database.db import get_db
from src.conf.config import config
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])

rate_limit_store = {}

MAX_REQUESTS = 2
TIME_WINDOW = timedelta(minutes=1)


@router.get("/me", response_model=User)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):

    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    pass
