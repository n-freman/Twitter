from fastapi import APIRouter, Depends

from twitter.presentation.schemas.tweet import (
    CreateTweetSchema,
    DeleteTweetSchema,
    UpdateTweetSchema
)
from twitter.services.auth import get_current_active_user

router = APIRouter(prefix='tweets')


@router.post('/create')
def create_tweet(
    tweet: CreateTweetSchema,
    user: Depends(get_current_active_user)
):
    pass


@router.delete('/delete')
def delete_tweet(
    tweet: DeleteTweetSchema,
    user: Depends(get_current_active_user)
):
    pass


@router.patch('/update')
def update_tweet(
    tweet: UpdateTweetSchema,
    user: Depends(get_current_active_user)
):
    pass


@router.put('/edit')
def edit_tweet(
    tweet: UpdateTweetSchema,
    user: Depends(get_current_active_user)
):
    pass
