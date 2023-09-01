from gavel.models import db
from datetime import datetime

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    annotator_id = db.Column(db.Integer, db.ForeignKey('annotator.id'))
    annotator = db.relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship('Item', foreign_keys=[item_id], uselist=False)
    comment = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, annotator, item, comment):
        self.annotator = annotator
        self.item = item
        self.comment = comment
