from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import traceback
import uvicorn

from app.database.database import engine, get_db, Base
from app.models.comment import Comment as CommentModel
from app.schemas.comment import Comment as CommentSchema
from app.schemas.comment import CommentCreate

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Comment Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "traceback": traceback.format_exc()
        }
    )

@app.get("/")
async def read_root():
    return {
        "message": "Comment Platform API",
        "status": "running",
        "port": "4343"
    }

@app.post("/comments/", response_model=CommentSchema)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    try:
        db_comment = CommentModel(
            content=comment.content,
            url=comment.url,
            parent_id=comment.parent_id
        )
        
        db_comment.ai_response = "AI response placeholder"
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    except Exception as e:
        db.rollback()
        print(f"Error creating comment: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/comments/", response_model=List[CommentSchema])
async def get_comments(url: str, db: Session = Depends(get_db)):
    return db.query(CommentModel).filter(CommentModel.url == url).all()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4343)