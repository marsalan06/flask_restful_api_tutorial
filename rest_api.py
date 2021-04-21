from flask import Flask
from flask.globals import session
from flask_restful import Api,Resource, abort, reqparse, marshal_with, fields
from data_sample import names
from flask_sqlalchemy import SQLAlchemy #get flask sql alchemy
#from db_config import VideoModel
import db_config

app=Flask(__name__)
api=Api(app) #using the module flask_restfull's Api class
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/flask_apil'
#database is to be created before hand, create database flask_apil;
db=SQLAlchemy(app) #created instance and imported

video_put_args=reqparse.RequestParser() #parser object for the data passed with the request of video 
video_put_args.add_argument("name",type=str,help="Name must be parsed",required=True)
#add argument method of the RequestParser validates the data passed with the help msg in case of fail
video_put_args.add_argument("views",type=int,help="Views must be parsed",required=True) 
video_put_args.add_argument("likes",type=int,help="Likes must be parsed",required=True) 

#for patch endpoint we create a new parser object but without the required argument
video_update_args=reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="Name must be parsed")
#add argument method of the RequestParser validates the data passed with the help msg in case of fail
video_update_args.add_argument("views",type=int,help="Views must be parsed") 
video_update_args.add_argument("likes",type=int,help="Likes must be parsed") 

class HelloWorld(Resource): #resource defined 
    def get (self,name): #a get method is created , it overides the requests.get method to return what is provided
        #bellow 
        #return {"data":"Hello World"} #json returned so its serializable 
        #return {"name":name,"age":age} #place age as keyword argument in the fuction 
        return names[name] #get data related to name provided from dictionary 

    def post(self): #creating post method to overide the requests method 
        return {'data':"posted"} #just for simple test 


#videos={} #empty dict to store video

#def video_id_not_present(video_id): #call this fucntion in the class video's methods
#     if video_id not in videos:
#         abort(404,message="video id not valid") #fucntion sends an erorr msg back if called with status code

#def video_id_present(video_id): #checks if the video is their so dont create it
#     if video_id in videos:
#         abort(409,message="Video already exist with the id")


#to create resource field and marshalling we use a dictionary with field objects 
resource_fields={
    "id":fields.Integer,
    "name":fields.String,
    "views":fields.Integer,
    "likes":fields.Integer
}

class Video(Resource): 
    @marshal_with(resource_fields)  #created a decorator for videomodel serialization
    def get(self,video_id): #youtube uses video id's
    
        # print(videos)
        # video_id_not_present(video_id) #check created to avoid crash
        # return videos[video_id] #get the video from the dictionary 

        #for data base we use the video model
        result=db_config.VideoModel.query.filter_by(id=video_id).first() #instance of the class is in result, require serilization
        print(result)
        if not result:
            abort(404,message="Couldnt find video by id")
        return result #requires serialization 

    @marshal_with(resource_fields)
    def put(self, video_id): #create a video
        #using the feilds and marshaling for videoModel 
        args=video_put_args.parse_args() #get the valid parsed arguments 
        result=db_config.VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="Video id already exist") #acts as a check to verify any repeting id 
        video=db_config.VideoModel(id=video_id,name=args["name"],views=args["views"],likes=args["likes"]) #created new videoModel
        db.session.add(video)
        db.session.commit()
        return video

        # #video_id_present(video_id)
        
        # #the data we want to parse with the request include name, views, likes so we'll use the parser
        # args=video_put_args.parse_args() #to get the validated parsed arguments 
        # #return {video_id:args} #to get return the data parsed
        
        # videos[video_id]=args #we create an entry in the dictionary 
        # return videos[video_id], 201 #returns the video id 
    

    @marshal_with(resource_fields)
    def patch(self,video_id):
        args=video_update_args.parse_args()
        #result=db_config.VideoModel.query.filter_by(id=video_id).first() #this doesnt update the model due to orm issue
        result=db.session.query(db_config.VideoModel).filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video doesnt exist do cant update")
        if args["name"]: #if parser doesnt get a value it places None, in case of required=True not placed
            #so we check every entry , wether its filled or not 
            print(args["name"])
            a=args["name"]
            result.name=a
        if args["views"]:
            print(args["views"])
            a=args["views"]
            result.views=a
        if args["likes"]:
            print(args["likes"])
            a=args["likes"]
            result.likes=a
        db.session.commit() #in case of patch or update return result 
        return result               

    @marshal_with(resource_fields)
    def delete (self,video_id):
        #video_id_not_present(video_id) #check if id not present 
        #del videos[video_id]
        #return '',204 #status code sent, not json so use response only 
        result=db.session.query(db_config.VideoModel).filter_by(id=video_id).first() #instance of the class is in result, require serilization
        print(result)
        if not result:
            abort(404,message="Couldnt find video by id to delete")
        db.session.delete(result)
        db.session.commit()
        return "deletion performed",200



api.add_resource(HelloWorld,"/helloworld/<string:name>") #resource is registered with endpoint /helloworld
api.add_resource(Video,"/video/<int:video_id>") #making the endpoint for video api call 

if __name__=="__main__":
    app.run(debug=True)

