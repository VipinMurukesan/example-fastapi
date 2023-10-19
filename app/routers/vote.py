from typing import List, Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

# prefix simplifies routes and tags to help grouping in the swagger docs
router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    new_vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == new_vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" Post with post id {new_vote.post_id} cannot be found",
        )

    # added logic if vote for the same user who created post don't allow

    if post.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f" user {current_user.id} cannnot vote on post id {new_vote.post_id} created by {post.owner_id}",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == new_vote.post_id, models.Vote.user_id == current_user.id
    )

    existing_vote = vote_query.first()

    if new_vote.dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f" user {current_user.id} has already voted on post id {new_vote.post_id}",
            )

        vote = models.Vote(post_id=new_vote.post_id, user_id=current_user.id)
        db.add(vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote has been removed"}
