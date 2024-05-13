from pydantic import BaseModel, ConfigDict
from typing import List
from pydantic import BaseModel
from typing import List, Optional


# user schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    # playlists: List['Playlist'] = []
    podcasts: List['Podcast'] = []

    # class Config:
    #     orm_mode = True

class UserUpdate(User,UserCreate):
    pass

# playlist schemas
class PlaylistBase(BaseModel):
    name: str

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int

    # class Config:
    #     from_attributes = True


# podcast schemas
class PodcastBase(BaseModel):
    name: str
    url: str
    notes: Optional[str] = None

class PodcastCreate(PodcastBase):
    pass

class Podcast(PodcastBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    # playlist_id: Optional[int] = None

    # class Config:
    #     from_attributes = True


class Response(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
