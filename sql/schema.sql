CREATE TABLE marketing_spend (
    record_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    channel VARCHAR(50) NOT NULL,
    spend NUMERIC(10, 2) NOT NULL,
    impressions INT,
    clicks INT
);

CREATE TABLE sales_data (
    sale_record_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    channel VARCHAR(50) NOT NULL,
    conversions INT,
    revenue NUMERIC(10, 2) NOT NULL
);