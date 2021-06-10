
class Cache:
    def __init__(self):
        self.songs = [] # song = { name, file_ids {lyrics, chords, lead, slides} }
        self.services = [] # service = {id, date, extra, lead, band1, band2, band3, band4, song1, song2, song3, song4}
        self.slides = [] # { song, slides }
