CREATE TABLE IF NOT EXISTS member (
    email TEXT NOT NULL,
    instrument TEXT NOT NULL,
    CONSTRAINT PK_member PRIMARY KEY (email,instrument)
);
