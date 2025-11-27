-- =====================================
-- ENUM TYPES
-- =====================================

CREATE TYPE user_role_enum AS ENUM ('student', 'lecturer', 'admin');

CREATE TYPE space_type_enum AS ENUM ('individual', 'group', 'meeting', 'quiet');

CREATE TYPE space_status_enum AS ENUM ('available', 'unavailable', 'maintenance');

CREATE TYPE reservation_status_enum AS ENUM (
  'pending',
  'confirmed',
  'checked_in',
  'completed',
  'cancelled',
  'no_show'
);

CREATE TYPE penalty_type_enum AS ENUM (
  'no_show',
  'late_checkout',
  'damage',
  'unauthorized_use'
);

CREATE TYPE notification_type_enum AS ENUM (
  'reservation_created',
  'reservation_status_changed',
  'penalty_assigned',
  'system_announcement'
);


-- =====================================
-- TABLE: users
-- =====================================

CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255),
    role            user_role_enum NOT NULL DEFAULT 'student',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ
);

CREATE INDEX ix_users_email_active ON users(email, is_active);
CREATE INDEX ix_users_role         ON users(role);


-- =====================================
-- TABLE: spaces
-- =====================================

CREATE TABLE spaces (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    capacity        INT          NOT NULL CHECK (capacity > 0),
    type            space_type_enum NOT NULL,
    status          space_status_enum NOT NULL DEFAULT 'available',
    location        VARCHAR(255) NOT NULL,
    description     TEXT,
    equipment       JSONB,
    average_rating  NUMERIC(3,2) DEFAULT 0.0 CHECK (average_rating >= 0 AND average_rating <= 5),
    total_ratings   INT NOT NULL DEFAULT 0 CHECK (total_ratings >= 0),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ
);

CREATE INDEX ix_spaces_status_type     ON spaces(status, type);
CREATE INDEX ix_spaces_capacity        ON spaces(capacity);
CREATE INDEX ix_spaces_equipment_gin   ON spaces USING GIN (equipment);


-- =====================================
-- TABLE: reservations
-- =====================================

CREATE TABLE reservations (
    id                  SERIAL PRIMARY KEY,
    user_id             INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    space_id            INT NOT NULL REFERENCES spaces(id) ON DELETE CASCADE,
    start_time          TIMESTAMPTZ NOT NULL,
    end_time            TIMESTAMPTZ NOT NULL,
    status              reservation_status_enum NOT NULL DEFAULT 'pending',
    check_in_time       TIMESTAMPTZ,
    check_out_time      TIMESTAMPTZ,
    qr_code_data        TEXT,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ,

    CONSTRAINT chk_reservation_time CHECK (end_time > start_time),

    -- Slot 1 giờ cố định (nếu không muốn constraint này thì xóa)
    CONSTRAINT chk_reservation_1h CHECK (
        end_time = start_time + INTERVAL '1 hour'
    )
);

-- Không cho đặt trùng suất cùng phòng
CREATE UNIQUE INDEX uq_reservation_space_slot
    ON reservations(space_id, start_time);

CREATE INDEX ix_reservations_user
    ON reservations(user_id, start_time DESC);

CREATE INDEX ix_reservations_space_time
    ON reservations(space_id, start_time);

CREATE INDEX ix_reservations_status
    ON reservations(status);


-- =====================================
-- TABLE: ratings
-- =====================================

CREATE TABLE ratings (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    admin_id        INT NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    reservation_id  INT NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    score           INT NOT NULL CHECK (score BETWEEN 1 AND 5),
    comment         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Một reservation chỉ được rate một lần
    CONSTRAINT uq_ratings_reservation UNIQUE (reservation_id)
);

CREATE INDEX ix_ratings_user  ON ratings(user_id);
CREATE INDEX ix_ratings_admin ON ratings(admin_id);


-- =====================================
-- TABLE: penalties
-- =====================================

CREATE TABLE penalties (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reservation_id  INT REFERENCES reservations(id) ON DELETE SET NULL,
    penalty_type    penalty_type_enum NOT NULL,
    points          INT NOT NULL CHECK (points > 0),
    reason          TEXT,
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_penalties_user        ON penalties(user_id);
CREATE INDEX ix_penalties_user_expiry ON penalties(user_id, expires_at);


-- =====================================
-- TABLE: notifications
-- =====================================

CREATE TABLE notifications (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            notification_type_enum NOT NULL,
    title           VARCHAR(255) NOT NULL,
    body            TEXT NOT NULL,
    reservation_id  INT REFERENCES reservations(id) ON DELETE SET NULL,
    penalty_id      INT REFERENCES penalties(id) ON DELETE SET NULL,
    is_read         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_notifications_user_created
    ON notifications(user_id, created_at DESC);

CREATE INDEX ix_notifications_unread
    ON notifications(user_id, is_read)
    WHERE is_read = FALSE;

-- =====================================
-- TABLE: utilities
-- =====================================

CREATE TABLE utilities (
    id          SERIAL PRIMARY KEY,
    key         VARCHAR(50) NOT NULL UNIQUE,
    label       VARCHAR(100) NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ
);

CREATE INDEX ix_utilities_key ON utilities(key);

-- =====================================
-- TABLE: ratings
-- =====================================

CREATE TABLE ratings (
    id          SERIAL PRIMARY KEY,
    booking_id  INTEGER NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating      INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment     TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ
);

CREATE INDEX ix_ratings_booking_id ON ratings(booking_id);
CREATE INDEX ix_ratings_user_id ON ratings(user_id);

