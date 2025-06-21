-- 1. Справочники и основные сущности
CREATE TABLE roles
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE users
(
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id       INTEGER REFERENCES roles (id)
);

CREATE TABLE categories
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE tags
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE orders
(
    id         SERIAL PRIMARY KEY,
    user_id    INT NOT NULL,
    order_date TIMESTAMP   DEFAULT NOW(),
    status     VARCHAR(50) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- 2. Основные сущности, которые ссылаются на справочники
CREATE TABLE posts
(
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users (id),
    title       VARCHAR(200) NOT NULL,
    content     TEXT         NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER REFERENCES categories (id)
);

CREATE TABLE products
(
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(200)   NOT NULL,
    order_id INT            NOT NULL,
    price    DECIMAL(10, 2) NOT NULL,
    stock    INT            NOT NULL CHECK (stock >= 0),
    FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
);

CREATE TABLE messages
(
    id          SERIAL PRIMARY KEY,
    sender_id   INTEGER REFERENCES users (id),
    receiver_id INTEGER REFERENCES users (id),
    content     TEXT NOT NULL,
    sent_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE attachments
(
    id          SERIAL PRIMARY KEY,
    post_id     INTEGER REFERENCES posts (id),
    file_path   VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Таблицы для связей и зависимые
CREATE TABLE post_tags
(
    post_id INTEGER REFERENCES posts (id),
    tag_id  INTEGER REFERENCES tags (id),
    PRIMARY KEY (post_id, tag_id)
);

CREATE TABLE likes
(
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES users (id),
    post_id    INTEGER REFERENCES posts (id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments
(
    id         SERIAL PRIMARY KEY,
    post_id    INTEGER REFERENCES posts (id),
    user_id    INTEGER REFERENCES users (id),
    content    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items
(
    id         SERIAL PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);
