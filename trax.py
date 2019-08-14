#!/usr/bin/env python
#  trax.py helpers for the yptrax app 

""" Contains 'helper' classes for managing search.Documents.
BaseDocumentManager provides some common utilities, and the Track subclass
adds some Track-document-specific helper methods.
"""

import csv
trax=[]
albums={}
artists={}

def aname(name):
    if not name or name in ("None","<Unknown>"):
        return None 
    elif name.startswith("The "):
        return name[4:]
    else:
        return name

def load_trax():
    infile = csv.DictReader(open("trax.csv"),delimiter='\t')
    for line in infile: 
        track = dict(line)
        track["id"]=len(trax)       
        artist = aname(track["artist"])     
        album = aname(track["album"])       
        if artist and album:
            if artist not in artists.keys():    
                artists[artist] = { "name": track["artist"], "alb":[album], "trx":[] }
            elif album not in artists[artist]["alb"]:
                artists[artist]["alb"].append(album)  
            if album not in albums.keys():    
                albums[album] = { "name": track["album"], "art":[artist], "trx":[] }
            elif artist not in albums[album]["art"]:    
                albums[album]["art"].append(artist)
            artists[artist]["trx"].append(track["id"])              
            albums[album]["trx"].append(track["id"])              
            trax.append(track)              
    return trax
    
def get_albums(filter=''):
    if len(albums)==0:
        trax = load_trax()
    if filter in artists.keys():
        return [a for a in sorted(artists[filter]["alb"],key=lambda s: s.lower())]
    elif filter:
        return [a for a in sorted(albums.keys(), key=lambda s: s.lower()) if a.startswith(filter) and len(albums[a]["trx"])>5]
    else:
        return [a for a in sorted(albums.keys(), key=lambda s: s.lower()) if len(albums[a]["trx"])>5]


def get_artists(filter=''):
    if len(artists)==0:
        trax = load_trax()
    return [a for a in sorted(artists.keys(), key=lambda s: s.lower()) if filter in a and len(artists[a]["trx"])>20]

def get_track(id):
    if id in range(len(trax)):
        return trax[id]
    return None     

def get_tracks(filter=''):
    if len(artists)==0:
        trax=load_trax()
    if filter in artists.keys():
        return [get_track(t) for t in artists[filter]["trx"]]
    elif filter in albums.keys():
        return [get_track(t) for t in albums[filter]["trx"]]
    elif filter:
        return [t for t in trax if t["title"].startswith(filter)]
    elif not trax:
        trax=load_trax()
    return trax[:999]
    