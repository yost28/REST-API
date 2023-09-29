from typing import Union, Optional, Literal

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from fastapi import HTTPException
from app.models import UserModel
import names
import random

app = FastAPI()


user_universe=list()



user_universe=[]
user_db=[]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/universe")
def get_user_universe():
    output=[]
    for i in range(0,len(user_db)):
     
        output.append(user_db[i]['user_name'])
        
    user_universe=output
    return output


            



@app.get("/seed_users")
def seed_users():
    for i in range(10):
        name=(names.get_first_name())

        if name not in user_universe:
            user_universe.append(name)





    #For each user seed some friends from the universe
    for user in user_universe:
        friends=random.choices(user_universe, k=3)

        #friends cannot repeat
        friends = set(friends)

        #User cannot be friends with themselves
        if user in friends:
            friends.remove(user)

        print(f"{user} has friends {list(friends)}")
        user_db.append(dict(user_name=user, friends=friends))
    return "Users seeded"
    


#Read all users
@app.get("/users")
def read_all_users():
    return user_db


#Create
@app.post("/add_user")
def add_user(user:str, friends:list):
    for friend in friends:
        if friend not in user_universe:
            raise HTTPException(status_code=400, detail=f"Friend {friend} does not exist")
        
    user=user.capitalize()
    user_db.append(dict(user_name=user.capitalize(), friends=friends))



    

    return f"Added {user}"
   
    

#Read a single user by name
@app.get("/get_user/{name}")
def read_single_user(name):
    for i in range(0,len(user_db)):
     
        if user_db[i]['user_name'] == name:
            return (user_db[i])
        
#get user 2nd 3rd connections
#Read a single user by name
@app.get("/get_user_distance/{name}")
def get_user_connections(name):
    def find_current_friends():
        person_obj=None
        for i in range(0,len(user_db)):
        
            if user_db[i]['user_name'] == name:
                person_obj= (user_db[i])

        
        if person_obj ==None:
            return f"Person {name} not found"
        
        #Find friends of my friends that are not my current friends.
        current_friends = person_obj['friends']
        return current_friends
    
    def find_second_connections(current_friends):
        second_connections=[]

        #find second connection friends
        for i in range(0,len(user_db)):
            
            #find my friends list of my friend
            if user_db[i]['user_name'] in current_friends:
                second_connections.extend(user_db[i]["friends"])

                output=list(set(second_connections))

                #remove me and my friends from the output 
                for friend in current_friends:
                    if friend in output:
                        output.remove(friend)
                    if name in output:
                        output.remove(name)

        return output

    def find_third_connections(second_connection_friends):
        third_connections=[]

        #find second connection friends
        for i in range(0,len(user_db)):
            
            #find my friends list of my friend
            if user_db[i]['user_name'] in second_connection_friends:
                third_connections.extend(user_db[i]["friends"])

                output=list(set(third_connections))

                #remove me and my friends from the output 
                for friend in second_connection_friends:
                    if friend in output:
                        output.remove(friend)
                    if name in output:
                        output.remove(name)

        return output
  
    current_friends= find_current_friends()
    second_connection_friends=find_second_connections(current_friends)
    third_connections=find_third_connections(second_connection_friends)

    output_dict ={
        "user_name":name,
        "friends":current_friends,
        "2nd connections": second_connection_friends,
        "3rd connections":third_connections
    }
    

    return output_dict




        


            

#Update a user
@app.put("/edit_user/{name}")
def update_user_friends(name:str, friends:list):
    #handle error case
    for friend in friends:
        if friend not in user_universe:
            raise HTTPException(status_code=400, detail=f"Friend {friend} does not exist")

    for i in range(0,len(user_db)):
     
        if user_db[i]['user_name'] == name:
            user_db[i]['user_name']= name
            user_db[i]['friends']= friends

            return f"Updated {name}"
    return HTTPException(status_code=400, detail=f"User {name} not found")

    


@app.delete("/delete_user/{name}")
def delete_user(name):
    for i in range(0,len(user_db)):
     
        if user_db[i]['user_name'] == name:
            del (user_db[i])

            return f"Deleted {name}"

        # if person.user_name == name:
        # #typically want to delete whole user object. but because we have a small db just delete both.
        #     return(person)
    
