from typing import List, Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func

# prefix simplifies routes and tags to help grouping in the swagger docs
router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.PostReturn])
@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
    limit: int = 1000,
    skip: int = 0,
    search: Optional[str] = "",
):
    
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    posts = list(map(lambda x: x._mapping, posts))

    return posts


# @router.get("/me", response_model=List[schemas.PostReturn])
@router.get("/me", response_model=List[schemas.PostOut])
def get_user_posts(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .filter(models.Post.owner_id == current_user.id)
        .group_by(models.Post.id)
        .all()
    )

    posts = list(map(lambda x: x._mapping, posts))

    return posts


# @router.get("/{id}", response_model=schemas.PostReturn)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id={id} was not found",
        )

    # post = list(map(lambda x: x._mapping, post))

    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostReturn,
)
def create_post(
    new_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = models.Post(owner_id=current_user.id, **new_post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostReturn)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()
    return existing_post
