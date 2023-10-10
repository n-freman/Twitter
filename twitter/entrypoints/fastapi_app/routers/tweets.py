import json

from fastapi import APIRouter, Depends, Response

from twitter.domain.tweets import Tweet
from twitter.presentation.schemas.auth import UserInDBSchema
from twitter.presentation.schemas.tweet import CreateTweetSchema
from twitter.services.auth import get_current_active_user
from twitter.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter(prefix='/tweets')


@router.post('/create')
async def create_tweet(
    tweet: CreateTweetSchema,
    user: UserInDBSchema = Depends(get_current_active_user)
):
    with SqlAlchemyUnitOfWork() as uow:
        tweet = Tweet(
            user_id=user.id,
            **tweet.model_dump()
        )
        uow.tweets.add(tweet)
        uow.commit()
    return {'detail': 'Successfully created Tweet'}


@router.delete('/delete/{tweet_id}')
def delete_tweet(
    tweet_id: int,
    user: UserInDBSchema = Depends(get_current_active_user)
):
    with SqlAlchemyUnitOfWork() as uow:
        tweet = uow.tweets.get(Tweet.id == tweet_id)
        if tweet is None:
            return Response(
                content=json.dumps({'detail': 'Tweet not found'}),
                status_code=400
            )
        uow.tweets.delete(tweet)
        uow.commit()
    return {'detail': 'Successfully deleted Tweet'}


@router.patch('/update/{tweet_id}')
def update_tweet(
    tweet_id: int,
    user: UserInDBSchema = Depends(get_current_active_user)
):
    pass


@router.put('/edit/{tweet_id}')
def edit_tweet(
    tweet_id: int,
    user: UserInDBSchema = Depends(get_current_active_user)
):
    pass
