-- StadiumSense AI - Initial Schema & Seed Data

-- Stadium table
CREATE TABLE IF NOT EXISTS stadium (
    id          SERIAL PRIMARY KEY,
    stadium_name VARCHAR(255) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    country     VARCHAR(100) NOT NULL
);

-- Locations table
CREATE TABLE IF NOT EXISTS locations (
    id            SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    category      VARCHAR(50)  NOT NULL,
    stadium_id    INTEGER      NOT NULL REFERENCES stadium(id) ON DELETE CASCADE
);

-- FAQ table
CREATE TABLE IF NOT EXISTS faq (
    id       SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer   TEXT NOT NULL
);

-- Routes table
CREATE TABLE IF NOT EXISTS routes (
    id            SERIAL PRIMARY KEY,
    source        VARCHAR(255) NOT NULL,
    destination   VARCHAR(255) NOT NULL,
    accessibility BOOLEAN      NOT NULL DEFAULT FALSE
);

-- ============================================================
-- SEED DATA
-- ============================================================

-- Stadium
INSERT INTO stadium (stadium_name, city, country) VALUES
    ('Lusail Iconic Stadium', 'Lusail', 'Qatar');

-- Locations (15+ across all categories)
INSERT INTO locations (location_name, category, stadium_id) VALUES
    -- Gates
    ('Gate A - North Entrance',     'gate',        1),
    ('Gate B - South Entrance',     'gate',        1),
    ('Gate C - VIP Entrance',       'gate',        1),

    -- Seat Blocks
    ('Block 101 - Lower North',     'seat_block',  1),
    ('Block 201 - Upper South',     'seat_block',  1),
    ('Block 305 - Premium West',    'seat_block',  1),

    -- Restrooms
    ('Restroom - Level 1 North',    'restroom',    1),
    ('Restroom - Level 2 South',    'restroom',    1),
    ('Accessible Restroom - Gate A','restroom',    1),

    -- Food Courts
    ('Food Court - Main Concourse', 'food_court',  1),
    ('Food Court - Level 2 East',   'food_court',  1),

    -- Merchandise
    ('FIFA Store - Gate A',         'merchandise', 1),
    ('Merchandise Kiosk - Level 2', 'merchandise', 1),

    -- Medical
    ('First Aid Station - Gate B',  'medical',     1),
    ('Medical Center - Level 1',    'medical',     1),

    -- Parking
    ('Parking Zone P1 - North',     'parking',     1),
    ('Parking Zone P2 - South',     'parking',     1),

    -- Metro
    ('Lusail Metro Station',        'metro',       1);

-- FAQs (10 entries)
INSERT INTO faq (question, answer) VALUES
    ('What time do gates open?',
     'Gates open 3 hours before kickoff. VIP Gate C opens 4 hours before the match.'),

    ('Where can I find the nearest restroom?',
     'Restrooms are located on every level near the concourse. The nearest accessible restroom is at Gate A on Level 1.'),

    ('Is there parking available at the stadium?',
     'Yes, parking is available at Zone P1 (North) and Zone P2 (South). We recommend using metro for faster access.'),

    ('How do I get to the stadium by metro?',
     'Take the Lusail Metro Line to Lusail Metro Station, which is a 5-minute walk from Gate A.'),

    ('Where is the FIFA merchandise store?',
     'The official FIFA Store is located at Gate A near the main entrance. A merchandise kiosk is also available on Level 2.'),

    ('What items are prohibited inside the stadium?',
     'Prohibited items include outside food/drinks, umbrellas, large bags (over 30x20x15 cm), drones, and professional cameras.'),

    ('Are there accessible routes for wheelchair users?',
     'Yes, accessible routes are available from Gate A and the metro station. Accessible restrooms are on Level 1 near Gate A.'),

    ('Where is the first aid station?',
     'First Aid is located at Gate B on the ground floor, and the Medical Center is on Level 1 near section 101.'),

    ('Can I re-enter the stadium after leaving?',
     'Re-entry is permitted with a valid match ticket. Please check your ticket for specific re-entry conditions.'),

    ('Where is the food court?',
     'The main food court is on the Main Concourse between Gates A and B. A second food court is on Level 2 East side.');

-- Routes (5 entries, some with accessibility)
INSERT INTO routes (source, destination, accessibility) VALUES
    ('Lusail Metro Station',    'Gate A - North Entrance',   TRUE),
    ('Gate A - North Entrance', 'Block 101 - Lower North',   TRUE),
    ('Gate B - South Entrance', 'Block 201 - Upper South',   FALSE),
    ('Gate A - North Entrance', 'First Aid Station - Gate B', TRUE),
    ('Parking Zone P1 - North', 'Gate A - North Entrance',   FALSE);
