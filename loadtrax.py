import fnmatch
import os
import eyed3

def xstr(string):
    if string is None:
        return None 
    elif string.isdigit():
        return int(string)
    else:
        return str(''.join([i if ord(i) < 128 else '' for i in string]))

def get_trackinfo(mfile):
    track={ "file": mfile, "size": int(os.stat(mfile).st_size), "status":"ERROR" }
    try:
        afile=eyed3.load(mfile)
        if afile.tag:
            track["artist"]=xstr(afile.tag.artist)
            track["title"]=xstr(afile.tag.title)
            track["album"]=xstr(afile.tag.album)
            if afile.tag.track_num[0]:
                track["track_no"]=int(afile.tag.track_num[0])
            track["length"]=int(afile.info.time_secs) 
            track["status"]="OK"
    except:
        pass
    return track

matches = []
unmatches = []
for root, dirnames, filenames in os.walk('D:\\My Music'):
    for filename in fnmatch.filter(filenames, '*.mp3'):
        if len(unmatches)<1000 and len([n for n in filename if n in '<>?*'])==0:
            mfile=os.path.join(root, filename)
            track=get_trackinfo(mfile)
            if track["status"]=="ERROR":
                unmatches.append(track)
            elif track["status"]=="OK" :
                matches.append(track)
        else:
            print filename, "not valid"


for match in matches:
    new_name=