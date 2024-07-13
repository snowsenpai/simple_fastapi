from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
 
router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id '{id}' does not exist")
    return {"data": post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.CreatePost, db: Session = Depends(get_db), req_user_id: int = Depends(oauth2.get_current_user)):
    # unpack a dict: **dict
    post = models.Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@router.put("/{id}")
def put_post(id: int, payload: schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id '{id}' does not exist")
    
    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

@router.patch("/{id}")
def patch_post(id: int, payload: schemas.UpdatePost, db: Session = Depends(get_db)):
    # filter out None values, dictionary comprehension
    filtered_data = { k: v for k, v in payload.model_dump().items() if v is not None }
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id '{id}' does not exist")
    
    post_query.update(filtered_data, synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id '{id}' does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return { "message": f"post with id '{id}' has been deleted", "data": post} #* empty dict
