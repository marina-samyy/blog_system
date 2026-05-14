from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

class CommentRepository:
    def create(self, db: Session, comment_data: CommentCreate, user_id: int):
        new_comment = Comment(
            content=comment_data.content,
            post_id=comment_data.post_id,
            parent_id=comment_data.parent_id,
            author_id=user_id
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment

    def get_by_post(self, db: Session, post_id: int, skip: int = 0, limit: int = 10):
        return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

    def delete(self, db: Session, comment_id: int):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment:
            db.delete(comment)
            db.commit()
        return comment
    
    def update(self, db: Session, comment_id: int, comment_data: dict):
        comment = self.get_by_id(db, comment_id)
        if comment:
            for key, value in comment_data.items():
                setattr(comment, key, value)
            db.commit()
            db.refresh(comment)
        return comment

    def get_by_id(self, db: Session, comment_id: int):
        return db.query(Comment).filter(Comment.id == comment_id).first()