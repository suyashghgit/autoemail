CREATE TABLE public.mailing_list (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    email_sequence INTEGER DEFAULT 0,
    join_date TIMESTAMP WITH TIME ZONE NOT NULL,
    last_email_sent_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE public.sequence_mapping (
    sequence_id INT PRIMARY KEY,
    email_body TEXT,  -- Using TEXT for very long email content
    article_link VARCHAR(255)
);

select * from mailing_list;

INSERT INTO public.mailing_list (
    user_id,
    first_name,
    last_name,
    email_address,
    email_sequence,
    join_date,
    last_email_sent_at
) VALUES (
    1,
    'Suyash',
    'Ghimire',
    'suyashghimire3000@gmail.com',
    0,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO sequence_mapping (sequence_id, email_body, article_link) VALUES
(1, 'Welcome to our newsletter. This is your first email in the sequence.', 'https://example.com/article1'),
(2, 'Thank you for staying with us. Here''s your second update.', 'https://example.com/article2'),
(3, 'We hope you''re finding our content valuable. Here''s your third email.', 'https://example.com/article3'),
(4, 'Here''s your fourth email in the sequence.', 'https://example.com/article4'),
(5, 'Fifth email in your journey with us.', 'https://example.com/article5'),
(6, 'Sixth email with more valuable content.', 'https://example.com/article6'),
(9, 'Final follow-up email in the sequence.', 'https://example.com/article9');






INSERT INTO public.mailing_list (user_id, first_name, last_name, email_address, email_sequence, join_date, last_email_sent_at)
VALUES
  (2, 'Mary', 'Johnson', 'mary.j@email.net', 4, '2024-01-16 09:15:00-08:00', '2024-03-02 10:15:00-08:00'),
  (3, 'Robert', 'Williams', 'rwilliams@email.org', 1, '2024-01-17 10:45:00-08:00', '2024-03-01 15:30:00-08:00'),
  (4, 'Patricia', 'Brown', 'pbrown@email.com', 3, '2024-01-18 11:20:00-08:00', '2024-03-02 09:45:00-08:00'),
  (5, 'Michael', 'Jones', 'mjones@email.net', 5, '2024-01-19 13:10:00-08:00', '2024-03-01 16:20:00-08:00'),
  (6, 'Linda', 'Garcia', 'lgarcia@email.com', 2, '2024-01-20 14:30:00-08:00', '2024-03-02 11:10:00-08:00'),
  (7, 'James', 'Miller', 'james.miller@email.org', 6, '2024-01-21 15:45:00-08:00', '2024-03-01 13:25:00-08:00'),
  (8, 'Elizabeth', 'Davis', 'edavis@email.net', 1, '2024-01-22 16:20:00-08:00', '2024-03-02 14:40:00-08:00'),
  (9, 'William', 'Rodriguez', 'wrodriguez@email.com', 3, '2024-01-23 09:30:00-08:00', '2024-03-01 15:55:00-08:00'),
  (10, 'Barbara', 'Martinez', 'bmartinez@email.org', 4, '2024-01-24 10:45:00-08:00', '2024-03-02 16:15:00-08:00'),
  (11, 'David', 'Anderson', 'danderson@email.net', 2, '2024-01-25 11:15:00-08:00', '2024-03-01 09:30:00-08:00'),
  (12, 'Jennifer', 'Taylor', 'jtaylor@email.com', 5, '2024-01-26 13:20:00-08:00', '2024-03-02 10:45:00-08:00'),
  (13, 'Richard', 'Thomas', 'rthomas@email.org', 1, '2024-01-27 14:30:00-08:00', '2024-03-01 11:20:00-08:00'),
  (14, 'Maria', 'Moore', 'mmoore@email.net', 3, '2024-01-28 15:45:00-08:00', '2024-03-02 13:35:00-08:00'),
  (15, 'Charles', 'Jackson', 'cjackson@email.com', 6, '2024-01-29 16:20:00-08:00', '2024-03-01 14:50:00-08:00'),
  (16, 'Susan', 'White', 'swhite@email.org', 2, '2024-01-30 09:30:00-08:00', '2024-03-02 15:15:00-08:00'),
  (17, 'Joseph', 'Harris', 'jharris@email.net', 4, '2024-01-31 10:45:00-08:00', '2024-03-01 16:30:00-08:00'),
  (18, 'Margaret', 'Martin', 'mmartin@email.com', 1, '2024-02-01 11:15:00-08:00', '2024-03-02 09:45:00-08:00'),
  (19, 'Thomas', 'Thompson', 'tthompson@email.org', 3, '2024-02-02 13:20:00-08:00', '2024-03-01 10:20:00-08:00'),
  (20, 'Sandra', 'Garcia', 'sgarcia@email.net', 5, '2024-02-03 14:30:00-08:00', '2024-03-02 11:35:00-08:00'),
  (21, 'Christopher', 'Martinez', 'cmartinez@email.com', 2, '2024-02-04 15:45:00-08:00', '2024-03-01 13:50:00-08:00'),
  (22, 'Ashley', 'Robinson', 'arobinson@email.org', 4, '2024-02-05 16:20:00-08:00', '2024-03-02 14:15:00-08:00'),
  (23, 'Kevin', 'Clark', 'kclark@email.net', 6, '2024-02-06 09:30:00-08:00', '2024-03-01 15:30:00-08:00'),
  (24, 'Lisa', 'Rodriguez', 'lrodriguez@email.com', 1, '2024-02-07 10:45:00-08:00', '2024-03-02 16:45:00-08:00'),
  (25, 'Steven', 'Lewis', 'slewis@email.org', 3, '2024-02-08 11:15:00-08:00', '2024-03-01 09:20:00-08:00'),
  (26, 'Helen', 'Lee', 'hlee@email.net', 5, '2024-02-09 13:20:00-08:00', '2024-03-02 10:35:00-08:00'),
  (27, 'Jeff', 'Walker', 'jwalker@email.com', 2, '2024-02-10 14:30:00-08:00', '2024-03-01 11:50:00-08:00'),
  (28, 'Betty', 'Hall', 'bhall@email.org', 4, '2024-02-11 15:45:00-08:00', '2024-03-02 13:15:00-08:00'),
  (29, 'Jason', 'Allen', 'jallen@email.net', 1, '2024-02-12 16:20:00-08:00', '2024-03-01 14:30:00-08:00'),
  (30, 'Carol', 'Young', 'cyoung@email.com', 3, '2024-02-13 09:30:00-08:00', '2024-03-02 15:45:00-08:00'),
  (31, 'Timothy', 'King', 'tking@email.org', 6, '2024-02-14 10:45:00-08:00', '2024-03-01 16:20:00-08:00'),
  (32, 'Sarah', 'Wright', 'swright@email.net', 2, '2024-02-15 11:15:00-08:00', '2024-03-02 09:35:00-08:00'),
  (33, 'Eric', 'Lopez', 'elopez@email.com', 4, '2024-02-16 13:20:00-08:00', '2024-03-01 10:50:00-08:00'),
  (34, 'Karen', 'Hill', 'khill@email.org', 1, '2024-02-17 14:30:00-08:00', '2024-03-02 11:15:00-08:00'),
  (35, 'Edward', 'Scott', 'escott@email.net', 3, '2024-02-18 15:45:00-08:00', '2024-03-01 13:30:00-08:00'),
  (36, 'Nancy', 'Green', 'ngreen@email.com', 5, '2024-02-19 16:20:00-08:00', '2024-03-02 14:45:00-08:00'),
  (37, 'Ronald', 'Adams', 'radams@email.org', 2, '2024-02-20 09:30:00-08:00', '2024-03-01 15:20:00-08:00'),
  (38, 'Michelle', 'Baker', 'mbaker@email.net', 4, '2024-02-21 10:45:00-08:00', '2024-03-02 16:35:00-08:00'),
  (39, 'Anthony', 'Nelson', 'anelson@email.com', 6, '2024-02-22 11:15:00-08:00', '2024-03-01 09:50:00-08:00'),
  (40, 'Laura', 'Carter', 'lcarter@email.org', 1, '2024-02-23 13:20:00-08:00', '2024-03-02 10:15:00-08:00'),
  (41, 'Kevin', 'Mitchell', 'kmitchell@email.net', 3, '2024-02-24 14:30:00-08:00', '2024-03-01 11:30:00-08:00'),
  (42, 'Kimberly', 'Perez', 'kperez@email.com', 5, '2024-02-25 15:45:00-08:00', '2024-03-02 13:45:00-08:00'),
  (43, 'George', 'Roberts', 'groberts@email.org', 2, '2024-02-26 16:20:00-08:00', '2024-03-01 14:20:00-08:00'),
  (44, 'Amy', 'Turner', 'aturner@email.net', 4, '2024-02-27 09:30:00-08:00', '2024-03-02 15:35:00-08:00'),
  (45, 'Brian', 'Phillips', 'bphillips@email.com', 1, '2024-02-28 10:45:00-08:00', '2024-03-01 16:50:00-08:00'),
  (46, 'Angela', 'Campbell', 'acampbell@email.org', 3, '2024-02-29 11:15:00-08:00', '2024-03-02 09:15:00-08:00'),
  (47, 'Paul', 'Parker', 'pparker@email.net', 6, '2024-03-01 13:20:00-08:00', '2024-03-01 10:30:00-08:00'),
  (48, 'Amanda', 'Evans', 'aevans@email.com', 2, '2024-03-02 14:30:00-08:00', '2024-03-02 11:45:00-08:00'),
  (49, 'Kenneth', 'Edwards', 'kedwards@email.org', 4, '2024-03-03 15:45:00-08:00', '2024-03-01 13:20:00-08:00'),
  (50, 'Melissa', 'Collins', 'mcollins@email.net', 1, '2024-03-04 16:20:00-08:00', '2024-03-02 14:35:00-08:00'),
  (51, 'Jerry', 'Stewart', 'jstewart@email.com', 3, '2024-03-05 09:30:00-08:00', '2024-03-01 15:50:00-08:00'),
  (52, 'Deborah', 'Morris', 'dmorris@email.org', 5, '2024-03-06 10:45:00-08:00', '2024-03-02 16:15:00-08:00'),
  (53, 'Dennis', 'Rogers', 'drogers@email.net', 2, '2024-03-07 11:15:00-08:00', '2024-03-01 09:30:00-08:00'),
  (54, 'Rebecca', 'Reed', 'rreed@email.com', 4, '2024-03-08 13:20:00-08:00', '2024-03-02 10:45:00-08:00'),
  (55, 'Frank', 'Cook', 'fcook@email.org', 6, '2024-03-09 14:30:00-08:00', '2024-03-01 11:20:00-08:00'),
  (56, 'Sharon', 'Morgan', 'smorgan@email.net', 1, '2024-03-10 15:45:00-08:00', '2024-03-02 13:35:00-08:00'),
  (57, 'Raymond', 'Bell', 'rbell@email.com', 3, '2024-03-11 16:20:00-08:00', '2024-03-01 14:50:00-08:00'),
  (58, 'Nicole', 'Murphy', 'nmurphy@email.org', 5, '2024-03-12 09:30:00-08:00', '2024-03-02 15:15:00-08:00'),
  (59, 'Gregory', 'Bailey', 'gbailey@email.net', 2, '2024-03-13 10:45:00-08:00', '2024-03-01 16:30:00-08:00'),
  (60, 'Christine', 'Rivera', 'crivera@email.com', 4, '2024-03-14 11:15:00-08:00', '2024-03-02 09:45:00-08:00'),
  (61, 'Samuel', 'Cooper', 'scooper@email.org', 1, '2024-03-15 13:20:00-08:00', '2024-03-01 10:20:00-08:00'),
  (62, 'Shirley', 'Richardson', 'srichardson@email.net', 3, '2024-03-16 14:30:00-08:00', '2024-03-02 11:35:00-08:00'),
  (63, 'Jeffrey', 'Cox', 'jcox@email.com', 6, '2024-03-17 15:45:00-08:00', '2024-03-01 13:50:00-08:00'),
  (64, 'Helen', 'Howard', 'hhoward@email.org', 2, '2024-03-18 16:20:00-08:00', '2024-03-02 14:15:00-08:00'),
  (65, 'Terry', 'Ward', 'tward@email.net', 4, '2024-03-19 09:30:00-08:00', '2024-03-01 15:30:00-08:00'),
  (66, 'Judith', 'Torres', 'jtorres@email.com', 1, '2024-03-20 10:45:00-08:00', '2024-03-02 16:45:00-08:00'),
  (67, 'Roy', 'Peterson', 'rpeterson@email.org', 3, '2024-03-21 11:15:00-08:00', '2024-03-01 09:20:00-08:00'),
  (68, 'Frances', 'Gray', 'fgray@email.net', 5, '2024-03-22 13:20:00-08:00', '2024-03-02 10:35:00-08:00'),
  (69, 'Scott', 'Ramirez', 'sramirez@email.com', 2, '2024-03-23 14:30:00-08:00', '2024-03-01 11:50:00-08:00'),
  (70, 'Cheryl', 'James', 'cjames@email.org', 4, '2024-03-24 15:45:00-08:00', '2024-03-02 13:15:00-08:00'),
  (71, 'Stephen', 'Watson', 'swatson@email.net', 6, '2024-03-25 16:20:00-08:00', '2024-03-01 14:30:00-08:00'),
  (72, 'Martha', 'Brooks', 'mbrooks@email.com', 1, '2024-03-26 09:30:00-08:00', '2024-03-02 15:45:00-08:00'),
  (73, 'Walter', 'Kelly', 'wkelly@email.org', 3, '2024-03-27 10:45:00-08:00', '2024-03-01 16:20:00-08:00'),
  (74, 'Gloria', 'Sanders', 'gsanders@email.net', 5, '2024-03-28 11:15:00-08:00', '2024-03-02 09:35:00-08:00'),
  (75, 'Henry', 'Price', 'hprice@email.com', 2, '2024-03-29 13:20:00-08:00', '2024-03-01 10:50:00-08:00'),
  (76, 'Virginia', 'Bennett', 'vbennett@email.org', 4, '2024-03-30 14:30:00-08:00', '2024-03-02 11:15:00-08:00'),
  (77, 'Douglas', 'Wood', 'dwood@email.net', 1, '2024-03-31 15:45:00-08:00', '2024-03-01 13:30:00-08:00'),
  (78, 'Emma', 'Barnes', 'ebarnes@email.com', 3, '2024-04-01 16:20:00-08:00', '2024-03-02 14:45:00-08:00'),
  (79, 'Philip', 'Ross', 'pross@email.org', 6, '2024-04-02 09:30:00-08:00', '2024-03-01 15:20:00-08:00'),
  (80, 'Rose', 'Henderson', 'rhenderson@email.net', 2, '2024-04-03 10:45:00-08:00', '2024-03-02 16:35:00-08:00'),
  (81, 'Joyce', 'Coleman', 'jcoleman@email.com', 4, '2024-04-04 11:15:00-08:00', '2024-03-01 09:50:00-08:00'),
  (82, 'Bobby', 'Jenkins', 'bjenkins@email.org', 1, '2024-04-05 13:20:00-08:00', '2024-03-02 10:15:00-08:00'),
  (83, 'Victoria', 'Perry', 'vperry@email.net', 3, '2024-04-06 14:30:00-08:00', '2024-03-01 11:30:00-08:00'),
  (84, 'Dylan', 'Powell', 'dpowell@email.com', 5, '2024-04-07 15:45:00-08:00', '2024-03-02 13:45:00-08:00'),
  (85, 'Johnny', 'Long', 'jlong@email.org', 2, '2024-04-08 16:20:00-08:00', '2024-03-01 14:20:00-08:00'),
  (86, 'Kelly', 'Patterson', 'kpatterson@email.net', 4, '2024-04-09 09:30:00-08:00', '2024-03-02 15:35:00-08:00'),
  (87, 'Howard', 'Hughes', 'hhughes@email.com', 6, '2024-04-10 10:45:00-08:00', '2024-03-01 16:50:00-08:00'),
  (88, 'Kathryn', 'Flores', 'kflores@email.org', 1, '2024-04-11 11:15:00-08:00', '2024-03-02 09:15:00-08:00'),
  (89, 'Harold', 'Washington', 'hwashington@email.net', 3, '2024-04-12 13:20:00-08:00', '2024-03-01 10:30:00-08:00'),
  (90, 'Teresa', 'Butler', 'tbutler@email.com', 5, '2024-04-13 14:30:00-08:00', '2024-03-02 11:45:00-08:00'),
  (91, 'Ralph', 'Simmons', 'rsimmons@email.org', 2, '2024-04-14 15:45:00-08:00', '2024-03-01 13:20:00-08:00'),
  (92, 'Diana', 'Foster', 'dfoster@email.net', 4, '2024-04-15 16:20:00-08:00', '2024-03-02 14:35:00-08:00'),
  (93, 'Carlos', 'Gonzales', 'cgonzales@email.com', 1, '2024-04-16 09:30:00-08:00', '2024-03-01 15:50:00-08:00'),
  (94, 'Julia', 'Bryant', 'jbryant@email.org', 3, '2024-04-17 10:45:00-08:00', '2024-03-02 16:15:00-08:00'),
  (95, 'Russell', 'Alexander', 'ralexander@email.net', 6, '2024-04-18 11:15:00-08:00', '2024-03-01 09:30:00-08:00'),
  (96, 'Alice', 'Russell', 'arussell@email.com', 2, '2024-04-19 13:20:00-08:00', '2024-03-02 10:45:00-08:00'),
  (97, 'Bruce', 'Griffin', 'bgriffin@email.org', 4, '2024-04-20 14:30:00-08:00', '2024-03-01 11:20:00-08:00'),
  (98, 'Lois', 'Diaz', 'ldiaz@email.net', 1, '2024-04-21 15:45:00-08:00', '2024-03-02 13:35:00-08:00'),
  (99, 'Wayne', 'Hayes', 'whayes@email.com', 3, '2024-04-22 16:20:00-08:00', '2024-03-01 14:50:00-08:00'),
  (100, 'Marilyn', 'Myers', 'mmyers@email.org', 5, '2024-04-23 09:30:00-08:00', '2024-03-02 15:15:00-08:00');


DROP TABLE IF EXISTS mailing_list;


-- Drop existing sequence if it exists
DROP SEQUENCE IF EXISTS mailing_list_user_id_seq CASCADE;

-- Create new sequence
CREATE SEQUENCE mailing_list_user_id_seq;

-- Set the sequence's current value to the maximum user_id
SELECT setval('mailing_list_user_id_seq', COALESCE((SELECT MAX(user_id) FROM mailing_list), 0) + 1);

-- Alter the table to use the sequence
ALTER TABLE mailing_list ALTER COLUMN user_id SET DEFAULT nextval('mailing_list_user_id_seq');


  ALTER TABLE public.mailing_list ALTER COLUMN user_id SET DEFAULT nextval('mailing_list_user_id_seq');
-- If the sequence doesn't exist, create it first:
CREATE SEQUENCE IF NOT EXISTS mailing_list_user_id_seq;
ALTER TABLE mailing_list ALTER COLUMN user_id SET DEFAULT nextval('mailing_list_user_id_seq');
ALTER SEQUENCE mailing_list_user_id_seq OWNED BY mailing_list.user_id;



CREATE TABLE mailing_list (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    email_sequence INTEGER DEFAULT 0,
    join_date TIMESTAMP WITH TIME ZONE NOT NULL,
    last_email_sent_at TIMESTAMP WITH TIME ZONE NOT NULL
);


CREATE TABLE email_metrics (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES mailing_list(user_id),
    sequence_id INTEGER,
    message_id VARCHAR,
    status VARCHAR,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    opened_at TIMESTAMP,
    bounced_at TIMESTAMP
);

-- Create an index on contact_id for better query performance
CREATE INDEX idx_email_metrics_contact_id ON email_metrics(contact_id);

-- Create an index on sent_at for better date range queries
CREATE INDEX idx_email_metrics_sent_at ON email_metrics(sent_at);



CREATE TABLE mailing_list (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    phone_number VARCHAR(20),
    linkedin_url VARCHAR(255),
    email_sequence INTEGER DEFAULT 0,
    join_date TIMESTAMP WITH TIME ZONE NOT NULL,
    last_email_sent_at TIMESTAMP WITH TIME ZONE NOT NULL
);