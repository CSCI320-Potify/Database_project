truncate table "user" cascade;
truncate table friends cascade;
truncate table song cascade;


INSERT INTO "user"(username, password, email, last_access_date, creation_date, first_name, last_name) VALUES
    ('bobby1', 'password', 'bc1@gmail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'bobby', 'caves'),
    ('stacey2', 'password', 'sl2@gmail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'stacey', 'logan'),
    ('greg3', 'password', 'gt3@gmail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'greg', 'timmy'),
    ('rob4', 'password', 'robby4@gmail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Dr', 'Phil');

INSERT INTO friends("user", follows) values
    ('bobby1', 'stacey2'),
    ('stacey2', 'bobby1'),
    ('greg3', 'rob4'),
    ('rob4', 'bobby1');

INSERT INTO song("Title", length, "song_num", "release_date") values
    ('song 1', 1000, 1, 2021),
    ('song 2', 1000, 2, 2021),
    ('song 3', 1000, 3, 2021),
    ('song 4', 1000, 4, 2021),
    ('song 5', 1000, 5, 2021),
    ('song 6', 1000, 6, 2021);


