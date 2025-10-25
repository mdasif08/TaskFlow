-- ProjectPulse Database Initialization
-- This file is executed when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist (handled by POSTGRES_DB env var)
-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created by SQLAlchemy when the backend starts
-- This file can be used for any additional database setup if needed
