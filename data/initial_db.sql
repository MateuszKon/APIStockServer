--DROP TABLE IF EXISTS users;
--DROP TABLE IF EXISTS transactions;
--DROP TABLE IF EXISTS stocks;
--DROP TABLE IF EXISTS user_watch_stocks;
--DROP TABLE IF EXISTS stock_alerts;
--DROP TABLE IF EXISTS user_alerts;
--DROP TABLE IF EXISTS user_to_stock_alerts;


CREATE EXTENSION pgcrypto;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    );

-- INSERT INTO users (email, password) VALUES ('johndoe@mail.com', crypt('johnspassword', gen_salt('bf')));
-- SELECT id  FROM users WHERE email = 'johndoe@mail.com' AND password = crypt('johnspassword', password);


CREATE TABLE stocks(
    id SERIAL PRIMARY KEY,
    stock_name TEXT
);


CREATE TYPE transaction_type AS ENUM ('BUY', 'SELL');


CREATE TABLE transactions(
    id SERIAL PRIMARY KEY,
    stock_id INTEGER,
    user_id INTEGER,
    type transaction_type,
    quantity INTEGER,
    price FLOAT,
    time TIMESTAMP,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,
    CONSTRAINT fk_stock
        FOREIGN KEY(stock_id)
            REFERENCES stocks(id)
    );


CREATE TABLE user_watch_stocks(
    user_id INTEGER,
    stock_id INTEGER,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,
    CONSTRAINT fk_stock
        FOREIGN KEY(stock_id)
            REFERENCES stocks(id),
    PRIMARY KEY(user_id, stock_id)
);


CREATE TABLE stock_alerts(
    id SERIAL UNIQUE,
    stock_id INTEGER,
    traced_variable TEXT,
    update_frequency TIMESTAMP,
    previous_value FLOAT,
    current_value FLOAT,
    last_update TIMESTAMP,
    CONSTRAINT fk_stock
        FOREIGN KEY(stock_id)
            REFERENCES stocks(id),
    PRIMARY KEY(stock_id, traced_variable, update_frequency)
);


CREATE TABLE user_alerts(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
);


CREATE TABLE user_to_stock_alerts(
    user_alert_id INTEGER,
    stock_alert_id INTEGER,
    CONSTRAINT fk_user_alert
        FOREIGN KEY(user_alert_id)
            REFERENCES user_alerts(id)
            ON DELETE CASCADE,
    CONSTRAINT fk_stock_alert
        FOREIGN KEY(stock_alert_id)
            REFERENCES stock_alerts(id),
    PRIMARY KEY (user_alert_id, stock_alert_id)
);