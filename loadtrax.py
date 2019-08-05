import fnmatch
import os
import eyed3
eyed3.log.setLevel("ERROR")

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

def get_file(filepath):
    dirs = filepath.split('\\')[-3:]
    return '/'.join(dirs)
    
def get_tracklen(tsecs):
    if not tsecs:
        return 0
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
        
def get_trackinfo(mfile):
    track={ "file": xstr(mfile)[12:], "size": int(os.stat(mfile).st_size), "status":"ERR" }
    try:
        afile=eyed3.load(mfile)
        if afile.tag:
            artist=track["artist"]=xstr(afile.tag.artist)
            track["title"]=xstr(afile.tag.title)
            album=track["album"]=xstr(afile.tag.album)
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

t=0
unmatches = []
for root, dirnames, filenames in os.walk('D:\\My Music'):
    for filename in fnmatch.filter(filenames, '*.mp3'):
        if len(unmatches)<1000 and len([n for n in filename if n in '<>?*'])==0:
            mfile=os.path.join(root, filename)
            track=get_trackinfo(mfile)
            if track["status"]=="ERR":
                unmatches.append(track)
            elif track["status"]=="OK" :
                if t % 100 == 0:
                    print (t, track['file'])                
                trax.append(track)
                t+=1
        else:
            print filename, "not valid"

