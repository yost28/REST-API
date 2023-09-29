from pydantic import BaseModel, Field, constr
from typing import Literal, Optional, List, Any, Union, Dict
import datetime



class UserModel(BaseModel):
    user_name:str
    friends:list
