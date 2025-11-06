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

