-- ============================================================
-- ENUM TYPES
-- ============================================================

-- Booking status
CREATE TYPE booking_status_enum AS ENUM (
    'pending',
    'confirmed',
    'checked_in',
    'completed',
    'cancelled',
    'no_show'
);

-- Penalty types
CREATE TYPE penalty_type_enum AS ENUM (
    'no_show',
    'late_checkout',
    'rule_violation'
);


-- ============================================================
-- USERS TABLE
-- ============================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,

    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    penalty_count INT NOT NULL DEFAULT 0,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);


-- ============================================================
-- SPACES TABLE
-- ============================================================

CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    capacity INT NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);


-- ============================================================
-- BOOKINGS TABLE
-- ============================================================

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    space_id INT NOT NULL REFERENCES spaces(id) ON DELETE CASCADE,

    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,

    status booking_status_enum NOT NULL DEFAULT 'pending',

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Prevent double-booking for same space/time slot
CREATE UNIQUE INDEX uq_space_time_slot
ON bookings (space_id, start_time, end_time);


-- ============================================================
-- RATINGS TABLE
-- ============================================================

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,

    booking_id INT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    space_id INT NOT NULL REFERENCES spaces(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    score INT NOT NULL CHECK (score >= 1 AND score <= 5),

    comment TEXT,
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- A user can only rate a space ONCE per booking
CREATE UNIQUE INDEX uq_rating_per_booking ON ratings (booking_id);


-- ============================================================
-- PENALTIES TABLE
-- ============================================================

CREATE TABLE penalties (
    id SERIAL PRIMARY KEY,

    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    booking_id INT REFERENCES bookings(id) ON DELETE SET NULL,

    type penalty_type_enum NOT NULL,
    reason TEXT,
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- UTILITIES TABLE
-- ============================================================

CREATE TABLE utilities (
    id SERIAL PRIMARY KEY,

    key VARCHAR(50) NOT NULL UNIQUE,
    label VARCHAR(255) NOT NULL,
    description TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
