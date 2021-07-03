import json
import ast
import os

db_dir = os.path.join(os.path.dirname(__file__), './db/')
import sqlite3
from sqlite3 import Error

db_file = db_dir + 'redeemer.db'

class DB:

    def __init__(self, db_file):
       con = None
       try:
           con = sqlite3.connect(db_file)
           print(sqlite3.version)
           cur = con.cursor()
           #cur.execute("drop table service")
           #cur.execute("drop table song")
           cur.execute("""
           CREATE TABLE IF NOT EXISTS song (
           	    name text PRIMARY KEY,
           	    ccli text,
                notes text,
                lyrics_id text,
                chords_id text,
                lead_id text,
                slides_id text,
                slides text
            );
           """)
           cur.execute("""
           CREATE TABLE IF NOT EXISTS service (
           	    id integer PRIMARY KEY,
           	    date text NOT NULL,
           	    message text,
                lead text,
                band1 text,
                band2 text,
                band3 text,
                band4 text,
                song1 text,
                song2 text,
                song3 text,
                song4 text,
                song5 text,
                song6 text,
                email_status text,
                slides_email_status text,
           	    FOREIGN KEY (song1) REFERENCES song (name),
                FOREIGN KEY (song2) REFERENCES song (name),
                FOREIGN KEY (song3) REFERENCES song (name),
                FOREIGN KEY (song4) REFERENCES song (name),
                FOREIGN KEY (song5) REFERENCES song (name),
                FOREIGN KEY (song6) REFERENCES song (name)
           );""")
           con.commit()
       except Error as e:
           print(e)
       finally:
           if con:
               con.close()

    def get_service(self, id):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            service = cur.execute('SELECT * FROM service where id=:service_id', {'service_id': id})
            r = service.fetchall()
            if not r:
               return None
            r = self._db_to_service(r[0])
            con.commit()
            return r
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def get_services(self):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            services = cur.execute('SELECT * FROM service ORDER BY id desc')
            res = []
            for service in services:
                r = self._db_to_service(service)
                res.append(r)
            con.commit()
            return res
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def get_service_dates(self):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            services = cur.execute('SELECT id FROM service ORDER BY id desc')
            res = []
            if services:
                for service in services:
                    res.append(service[0])
            con.commit()
            return res
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def drop_services(self):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            cur.execute("delete from service")
            con.commit()
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def add_service(self, service):
        self.add_services([service])

    def add_services(self, services):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            for service in services:
                cur.execute("""
                insert into service(id, date, message, lead, band1, band2, band3, band4, song1, song2, song3, song4, song5, song6, email_status, slides_email_status)
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (      service['id'],\
                            service['date'],\
                            service.get('message', ''),\
                            service.get('lead', ''),\
                            service.get('band1', ''),\
                            service.get('band2', ''),\
                            service.get('band3', ''),\
                            service.get('band4', ''),\
                            service.get('song1', ''),\
                            service.get('song2', ''),\
                            service.get('song3', ''),\
                            service.get('song4', ''),\
                            service.get('song5', ''),\
                            service.get('song6', ''),\
                            service.get('email_status', 'not sent test'),\
                            service.get('slides_email_status', 'not sent test')))
            con.commit()
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def update_service(self, service):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            cur.execute("""
                update service set(date, message, lead, band1, band2, band3, band4, song1, song2, song3, song4, song5, song6, email_status, slides_email_status)=( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                where(id = ?)
                """,(   service['date'],\
                        service.get('message', ''),\
                        service.get('lead', ''),\
                        service.get('band1', ''),\
                        service.get('band2', ''),\
                        service.get('band3', ''),\
                        service.get('band4', ''),\
                        service.get('song1', ''),\
                        service.get('song2', ''),\
                        service.get('song3', ''),\
                        service.get('song4', ''),\
                        service.get('song5', ''),\
                        service.get('song6', ''),\
                        service.get('email_status', 'not sent test'),\
                        service.get('slides_email_status', 'not sent test'),\
                        service['id']))
            con.commit()
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def get_song(self, name):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            songs = cur.execute('SELECT * FROM song where name=:song_name', {'song_name': name})
            r = songs.fetchall()
            if not r:
               return None
            r = self._db_to_song(r[0])
            con.commit()
            return r
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def get_songs(self):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            songs = cur.execute('SELECT * FROM song ORDER BY name')
            res = []
            for song in songs:
                r = self._db_to_song(song)
                res.append(r)
            con.commit()
            return res
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def get_song_names(self):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            songs = cur.execute('SELECT name FROM song ORDER BY name')
            res = []
            for song in songs:
                res.append(song[0])
            con.commit()
            return res

        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def drop_songs(self):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            cur.execute("delete from song")
            con.commit()
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def add_song(self, song):
        return self.add_songs([song])

    def add_songs(self, songs):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            for song in songs:
                cur.execute("""
                insert into song(name, ccli, notes, lyrics_id, chords_id, lead_id, slides_id, slides)
                values(?, ?, ?, ?, ?, ?, ?, ?);
                """, (song['name'],\
                            song.get('ccli', ''),\
                            song.get('notes', ''),\
                            song['file_ids'].get('lyrics', None),\
                            song['file_ids'].get('chords', None),\
                            song['file_ids'].get('lead', None),\
                            song['file_ids'].get('slides', None),\
                            song.get('slides', '')))
            con.commit()
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def update_song(self, song):
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            cur.execute("""
                update song set(ccli, notes, lyrics_id, chords_id, lead_id, slides_id, slides)=(?, ?, ?, ?, ?, ?, ?)
                where(name = ?)
                """,(song.get('ccli', ''),\
                song.get('notes', ''),\
                song['file_ids'].get('lyrics', None),\
                song['file_ids'].get('chords', None),\
                song['file_ids'].get('lead', None),\
                song['file_ids'].get('slides', None),\
                song.get('slides', ''),\
                song.get('name')))
            con.commit()
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def _db_to_song(self, song):
        r = {}
        r['name'] = song[0]
        r['ccli'] = song[1]
        r['notes'] = song[2]
        r['file_ids'] = {}
        r['file_ids']['lyrics'] = song[3]
        r['file_ids']['chords'] = song[4]
        r['file_ids']['lead'] = song[5]
        r['file_ids']['slides'] = song[6]
        r['slides'] = song[7]
        return r

    def _db_to_service(self, service):
        r = {}
        r['id'] = service[0]
        r['date'] = service[1]
        r['message'] = service[2]
        r['lead'] = service[3]
        r['band1'] = service[4]
        r['band2'] = service[5]
        r['band3'] = service[6]
        r['band4'] = service[7]
        r['song1'] = service[8]
        r['song2'] = service[9]
        r['song3'] = service[10]
        r['song4'] = service[11]
        r['song5'] = service[12]
        r['song6'] = service[13]
        r['email_status'] = service[14]
        r['slides_email_status'] = service[15]
        return r

db = DB(db_file)
