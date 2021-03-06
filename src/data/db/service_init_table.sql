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
);
