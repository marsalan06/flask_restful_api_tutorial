from flask import views
import requests 

BASE="http://127.0.0.1:5000/"

#response= requests.get(BASE+ "helloworld") #send an http get request on the base path and endpoint

#created the post request 
#response= requests.post(BASE+ "helloworld") #send an http post request on the base path and endpoint

#passed data with the url to the get method, we can pass variable storing data as well
#response= requests.get(BASE+ "helloworld/Arsalan") #send an http get request with data 

#for video test we use a dictionary format as json to send data 
# response=requests.put(BASE+"video/3",{"name":"video 3","views":120,"likes":12})

# print(response.json()) #returns a json object  

# input() #press enter 

# #delete a particular video
# response=requests.delete(BASE+"video/2")
# print(response) #not getting a json serilizable response from api 

# #get the dict of videos for particular video
# response=requests.get(BASE+"video/2")
# print(response.json()) #same response for validation of complete entry

#using videomodel to enter multiple videos 

# data =[{"likes":34,"name":"joe","views":2134},
#         {"likes":154,"name":"asdfd","views":244},
#         {"likes":4,"name":"monoplfo","views":521}
# ]

# for i in range(len(data)):
#     response=requests.put(BASE+"video/"+str(i+1),data[i]) #data has the dict of data pasrsed, to resolve conflict of ids we added +1
#     print(response.json())


# response=requests.patch(BASE+"video/3",{"name":"video3+"})
# print(response.json())

# response=requests.delete(BASE+"video/3")
# print(response)
response=requests.put(BASE+"video/3",{"name":"video3","views":234,"likes":342})
print(response.json())

input()
response=requests.get(BASE+"video/3")
print(response.json())