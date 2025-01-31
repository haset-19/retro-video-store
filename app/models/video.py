from sqlalchemy.orm import backref
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer, nullable=True)
    customers = db.relationship("Customer", secondary="rental", back_populates="videos")
   
    def to_dict(self):
        """converts task data to dictionary"""
        result = {"id": self.video_id,
                  "title": self.title,
                  "release_date": self.release_date,
                  "total_inventory": self.total_inventory
                  }
        return result

  
    def __str__(self) -> str:
        return "Video"
