songList = [
        {
            "chords": "https://docs.google.com/document/d/1vhY8DxYbViWgIY48WSNJNINZo36L_mmUBLE87CZAYak/edit?usp=sharing",
            "id": 0,
            "lyrics": "https://drive.google.com/file/d/1bQbSIrJXTbG9UzXPum3k-T8lW-aUQ9RL/view?usp=sharing",
            "name": "To God Be The Glory"
        }
    ]
presentations = [
        {
            "id": 0,
            "slides": [
                [
                    "To God be the glory, great things he has done!",
                    "so loved he the world that he gave us his Son",
                    "who yielded his life an atonement for sin,",
                    "and opened the life-gate that all may go in."
                ],
                [
                    "Praise the Lord, praise the Lord!",
                    "Let the earth hear his voice!",
                    "Praise the Lord, praise the Lord!",
                    "Let the people rejoice!",
                    "O come to the Father through Jesus the Son",
                    "and give him the glory great things he has done."
                ],
                [
                    "O perfect redemption, the purchase of blood!",
                    "To every believer the promise of God:",
                    "the vilest offender who truly believes,",
                    "that moment from Jesus a pardon receives."
                ],
                [
                    "Praise the Lord, praise the Lord!",
                    "Let the earth hear his voice!",
                    "Praise the Lord, praise the Lord!",
                    "Let the people rejoice!",
                    "O come to the Father through Jesus the Son",
                    "and give him the glory great things he has done."
                ],
                [
                    "Great things he has taught us, great things he has done,",
                    "and great our rejoicing through Jesus the Son:",
                    "but purer and higher and greater will be",
                    "our joy and our wonder, when Jesus we see!"
                ],
                [
                    "Praise the Lord, praise the Lord!",
                    "Let the earth hear his voice!",
                    "Praise the Lord, praise the Lord!",
                    "Let the people rejoice!",
                    "O come to the Father through Jesus the Son",
                    "and give him the glory great things he has done."
                ]
            ]
        }
    ]

def find_song(id):
    for song in songList:
        if id == song['id']:
            return song['name']
    raise "No song"

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
