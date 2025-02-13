-- Instead of dropping and recreating the database, we'll just create tables if they don't exist
-- Remove these lines:
-- DROP DATABASE IF EXISTS local;
-- CREATE DATABASE local;
-- \c local;

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS public.email_metrics (
    -- ... existing table definition ...
);

-- Add other CREATE TABLE IF NOT EXISTS statements

-- Now include your table creation scripts
-- They will run on a fresh database