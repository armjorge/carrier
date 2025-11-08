-- Create schema 
CREATE SCHEMA IF NOT EXISTS {schema_name};

-- Create companies type table
CREATE TABLE IF NOT EXISTS {schema_name}.company_types (
    {table_company_types}
);

-- Create companies table
CREATE TABLE IF NOT EXISTS {schema_name}.companies (
    {table_companies}
);

-- Create applications table
CREATE TABLE IF NOT EXISTS {schema_name}.applications (
    {table_applications}
);

-- Create languages table
CREATE TABLE IF NOT EXISTS {schema_name}.languages (
    {table_languages}
);

-- Create cover letters table
CREATE TABLE IF NOT EXISTS {schema_name}.cover_letters (
    {table_cover_letters}
);

-- Crear trigger
CREATE OR REPLACE FUNCTION {schema_name}.insert_cover_letter()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO {schema_name}.cover_letters (job, lang, company_name)
    VALUES (NEW.job, NEW.lang, NEW.company_name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- correr trigger
CREATE OR REPLACE FUNCTION {schema_name}.insert_cover_letter()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO {schema_name}.cover_letters (job, lang, company_name)
    VALUES (NEW.job, NEW.lang, NEW.company_name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;