from gavel.models import db
import gavel.crowd_bt as crowd_bt
from sqlalchemy.orm.exc import NoResultFound
from urllib.parse import urlparse


view_table = db.Table('view',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('annotator_id', db.Integer, db.ForeignKey('annotator.id'))
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    video = db.Column(db.Text, nullable=False)
    preso = db.Column(db.Text, nullable=False)
    folder = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    viewed = db.relationship('Annotator', secondary=view_table)
    prioritized = db.Column(db.Boolean, default=False, nullable=False)

    mu = db.Column(db.Float)
    sigma_sq = db.Column(db.Float)

    def __init__(self, name, location, description, category="None", video="None", preso="None", folder="None"):
        self.name = name
        self.location = location
        self.description = description
        self.video = Item.process_video_link(video)
        self.preso = preso
        self.folder = folder
        self.mu = crowd_bt.MU_PRIOR
        self.sigma_sq = crowd_bt.SIGMA_SQ_PRIOR
        self.category = category

    @classmethod
    def by_id(cls, uid):
        if uid is None:
            return None
        try:
            item = cls.query.get(uid)
        except NoResultFound:
            item = None
        return item

    @staticmethod
    def process_video_link(link):
        # Parse URL, if it's a Google file assume it's a video and reformat the URL
        o = urlparse(link)
        # If file link path starts with `/open`
        if o.path.startswith('/open'):
            id = o.query
            return 'https://drive.google.com/file/d/' + id.strip('id=') + '/preview'
        # Sharing link
        elif o.path.startswith('/file'):
            paths = o.path.split('/')
            id = paths[3]
            return 'https://drive.google.com/file/d/' + id.strip('id=') + '/preview'
        else:
            return link

