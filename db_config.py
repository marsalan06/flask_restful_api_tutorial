from rest_api import db #imported instance 


#orm technique to applied by the model 
class VideoModel(db.Model): #sqlalchemy model class
    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    views=db.Column(db.Integer,nullable=False)
    likes=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views},likes={self.likes})"

#db.create_all() #remove it after creating 