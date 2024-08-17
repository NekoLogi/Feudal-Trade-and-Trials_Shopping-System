CREATE TABLE itemroll (
    id INT PRIMARY KEY,
    tier INT NOT NULL DEFAULT 1,
    name VARCHAR(255) NOT NULL,
    displayname VARCHAR(255) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    enchantments VARCHAR(1000) NOT NULL,
    amount INT NOT NULL DEFAULT 0,
    sale INT NOT NULL DEFAULT 0
);