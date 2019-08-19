import fnmatch
import os
import json
import eyed3
from hurry.filesize import size
from shutil import copyfile
eyed3.log.setLevel("ERROR")

root_folder = "C:\\Users\\Steve Holtebeck\\Music"
artists = []
albums = {}
trax = []

def xstr(string):
    if string is None:
        return None 
    elif string.isdigit():
        return int(string)
    else:
        return str(''.join([i if ord(i) < 128 else '' for i in string]))

def find_track(path,trax):
    found=[t for t in trax if t["file"].endswith(path)]
    if len(found)==0:
        return None
    else:
        return found[0]

def load_trax():
    with open('static/trax.json') as trax_json:
        trax = json.load(trax_json)
    return trax

def aname(name):
    if name.startswith("The "):
        return name[4:]
    else:
        return name

def rname(path,delim):
    dirs=path.split(delim)
    if len(dirs)>2: 
        return '\\'.join(dirs[2:])   
    else:
        return None

def get_file(filepath):
    dirs = filepath.split('\\')[-3:]
    return '/'.join(dirs)

def get_files(folder,filter):
    files=[]
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, filter):
            files.append('\\'.join([root,filename]))
    return files
    
def get_tracklen(tsecs):
    if not tsecs:
        return 0
    elif ':' in str(tsecs):
        (m,s)=str(tsecs).split(':')
        return int(m)*60+int(s)     
    else:
        return str(int(tsecs/60))+':'+ "%02d" % (int(tsecs) % 60)

def write_trax(trax):
    delim='\t'
    keys=['artist','album','track_no','title', 'length','file', 'size']
    f=open('trax.csv','w')
    f.write(delim.join(keys)+'\n')
    for track in trax:
        f.write(delim.join([str(track.get(key)) for key in keys])+'\n')
    f.close()
    return len(trax)


def copy_file(song,old_folder,new_folder):
    old_name = old_folder + '\\' + song["file"]
    new_name = new_folder + '\\' + song["new_file"]
    copyfile(old_name,new_name)


def write_playlist(folder,trax):
    old_folder="F:\\My Music"
    if not os.path.exists(folder):
        os.mkdir(folder)
    fname=[f for f in folder.split('\\') if f][-1]+".m3u"
    tsize=size(sum([int(t.get("size",0)) for t in trax]))
    tlen=get_tracklen(sum([get_tracklen(t.get("length")) for t in trax]))
    f=open(folder+'\\'+fname,'w')
    f.write("# "+fname+" ("+str(len(trax))+" tracks, "+tlen+", "+tsize+")\n")    
    for track in trax:
#       copy_file(track,old_folder,folder)
        f.write(track["file"]+"\n")
    f.close()       
    return {"name": fname, "trax": len(trax), "length": tlen, "size": tsize }   
        
def get_trackinfo(mfile):
    track={ "file": xstr(mfile), "size": int(os.stat(mfile).st_size), "status":"ERR" }
    try:
        afile=eyed3.load(mfile)
        if afile.tag:
            artist=track["artist"]=xstr(afile.tag.artist)
            track["title"]=xstr(afile.tag.title)
            album=track["album"]=xstr(afile.tag.album)
            if afile.tag.album_artist:
                track["album_artist"]=xstr(afile.tag.album_artist)
            else:
                track["album_artist"]=track["artist"]
            if afile.tag.track_num[0]:
                track["track_no"]=int(afile.tag.track_num[0])
            track["length"]=get_tracklen(afile.info.time_secs) 
            if artist not in artists:
                artists.append(artist)
            if artist not in albums.keys():
                albums[artist]=[album]
            elif album not in albums[artist]:
                albums[artist].append(album)
            track["status"]="OK"
        else:
            dirs=mfile.split('\\')
    except:
        pass
    return track
    
def read_playlist(file,trax):
    songs=[]
    for song in [rname(line.strip(),'/') for line in open(file).readlines()]:
        track=find_track(song,trax)
        if track and track.get("title"):
            track["file"]=song
            track["track_no"]=len(songs)+1
            track["new_file"]='%02d_' % track["track_no"] + aname(track["artist"]) + "-" + track["title"] + song[-4:]
            track["new_file"]=track["new_file"].replace('?','').replace('/','+').replace('>','').replace('<','')
            songs.append(track)
    return songs

def load_all_files():
    mytrax=[]
    for mfile in get_files(root_folder,'*.mp3'):
        track=get_trackinfo(mfile)
        if track["status"]=="OK" :
            mytrax.append(track)
    return mytrax

def copy_playlist(playlist):
    songs=read_playlist(playlist,trax)
    artists=set([s["artist"] for s in songs])
    if len(artists)>2:
        pname=playlist[4:-4]
    else:
        pname=aname(artists.pop())
        for song in songs:
            song["new_file"] = song["new_file"].replace(pname+'-','')		
    if len(songs) in range(9,100):
        new_folder=root_folder+'\\'+pname
        playlist=write_playlist(new_folder,songs)
    return playlist

def fix_playlists():
    for playlist in get_files(root_folder,"*m3u"):
        folder='\\'.join(playlist.split('\\')[:-1])
        tracks=[get_trackinfo(file) for file in get_files(folder,"*mp3")]
        print(write_playlist(folder,tracks))
	
trax = load_trax()
plists= get_files("m3u","*m3u")

