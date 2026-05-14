from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.comment_repo import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.utils import cache 
from app.utils.comment_tree import build_comment_tree  # <-- DO NOT FORGET THIS

class CommentService:
    def __init__(self):
        self.repo = CommentRepository()

    def create_comment(self, db: Session, comment_data: CommentCreate, user_id: int):
        if comment_data.parent_id == 0:
            comment_data.parent_id = None
            
        new_comment = self.repo.create(db, comment_data, user_id)
        cache.delete_pattern(f"comments:post:{comment_data.post_id}:*")
        return new_comment

    def get_post_comments(self, db: Session, post_id: int, page: int = 1, size: int = 10):
        cache_key = f"comments:post:{post_id}:p:{page}:s:{size}"
        
        cached_data = cache.get_cache(cache_key)
        if cached_data:
            return cached_data

        skip = (page - 1) * size
        comments = self.repo.get_by_post(db, post_id, skip=skip, limit=size)
        
        serialized_comments = [
            {
                "id": c.id,
                "content": c.content,
                "author_id": c.author_id,
                "post_id": c.post_id,
                "parent_id": c.parent_id,
                "created_at": c.created_at.isoformat() if hasattr(c, 'created_at') and c.created_at else None
            }
            for c in comments
        ]

        # VITAL: Ensure this function uses dictionary ['key'] access!
        comments_tree = build_comment_tree(serialized_comments)

        cache.set_cache(cache_key, comments_tree)
        return comments_tree

    # ... rest of your methods (delete and update) are good ...

    def delete_comment(self, db: Session, comment_id: int, user_id: int, is_admin: bool):
        comment = self.repo.get_by_id(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        # 1. Clear cache before deleting so the GET request notices the change
        cache.delete_pattern(f"comments:post:{comment.post_id}:*")
        
        # 2. Perform deletion
        return self.repo.delete(db, comment_id)

    def update_comment(self, db: Session, comment_id: int, comment_data: CommentUpdate, user_id: int):
        comment = self.repo.get_by_id(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        if comment.author_id != user_id:
            raise HTTPException(status_code=403, detail="You can only edit your own comments")

        # Clear cache after update
        cache.delete_pattern(f"comments:post:{comment.post_id}:*")

        return self.repo.update(db, comment_id, comment_data.model_dump(exclude_unset=True))