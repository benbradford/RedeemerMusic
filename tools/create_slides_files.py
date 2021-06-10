songList = [

    ]
presentations = [

    ]

def find_song(id):
    for song in songList:
        if id == song['id']:
            return song['name']
    raise Exception("No song")

for slides in presentations:

    print "-------------------------------"
    name = find_song(slides['id'])
    file_name = "bin/slides/" + name + " (slides).txt"
    outF = open(file_name, "w")
    print ""
    for slide in slides['slides']:
        for line in slide:
            if line != "":
                line = line.replace('\u2014', '-').replace('\u2018', "'").replace('\u2019', '\'').replace('\u201c', "'").replace("\u201d", "'").replace("\u2013", "-")
                print line
                outF.write(line)
                outF.write("\n")
        print ""
        outF.write("\n")
    outF.write("\n")
    outF.close()
