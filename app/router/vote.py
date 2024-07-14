from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/posts", status_code=status.HTTP_201_CREATED)
def vote_post(payload: schemas.Vote, req_user: models.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    post_id = payload.post_id
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id '{post_id}' does not exist")
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == post_id, 
        models.Vote.user_id == req_user.id
        )
    existing_vote = vote_query.first()

    if(payload.vote_dir):
        if existing_vote:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"you have already voted on this post '{post_id}'")
        new_vote = models.Vote(post_id=post_id, user_id=req_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"you have voted on this post '{post_id}'"}
    else:
        if not existing_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"you have not voted on this post '{post_id}'")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"your vote on post '{post_id}' has been removed"}