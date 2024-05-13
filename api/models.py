from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from . import database


class User(database.Base):
  __tablename__='users'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String, unique=True, index=True)
  
  # playlists = relationship('Playlist', back_populates="owner")
  podcasts = relationship('Podcast', back_populates="owner")


# class Playlist(database.Base):
#   __tablename__="playlists"
#   id = Column(Integer, primary_key=True, index=True)
#   name = Column(String)

#   owner_id = Column(Integer, ForeignKey('users.id'))
#   owner = relationship("User", back_populates="playlists")

#   podcasts = relationship("Podcast", back_populates="playlist")


class Podcast(database.Base):
  __tablename__ = 'podcasts'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  url = Column(String)
  notes = Column(String)
  
  owner_id = Column(Integer, ForeignKey('users.id'))
  owner = relationship("User", back_populates="podcasts")
  
  # playlist_id = Column(Integer, ForeignKey('playlists.id'))
  # playlist = relationship("Playlist", back_populates="podcasts")