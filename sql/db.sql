CREATE DATABASE bookizon_books_knowledge_discovery;

CREATE TABLE time
(
    date_time_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    year         INT(4)              NOT NULL,
    month        INT(2)              NOT NULL,
    day          INT(2)              NOT NULL,
    hour         INT(2)              NOT NULL,
    minutes      INT(2)              NOT NULL
);

CREATE TABLE services
(
    service_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name       VARCHAR(255)        NOT NULL
);

CREATE TABLE customers
(
    customer_id           INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    gender                INT(1),
    birthday_date_time_id INT(11),
    foreign key (birthday_date_time_id) references time (date_time_id) on update cascade on delete set null
);

CREATE TABLE shops
(
    shop_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    lat     VARCHAR(255),
    `long`  VARCHAR(255)
);

CREATE TABLE books
(
    book_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    service_id INT(11),
    book_creation_date_id INT(11),
    book_date_id INT(11),
    customer_id INT(11),
    shop_id INT(11),
    price float,
    discount_price float,
    discount_perc float,
    duration INT(11),
    customer_age INT(3),
    platform VARCHAR(255),
    place_id INT(11),
    foreign key (service_id) references services (service_id) on update cascade on delete set null,
    foreign key (book_creation_date_id) references time (date_time_id) on update cascade on delete set null,
    foreign key (book_date_id) references time (date_time_id) on update cascade on delete set null,
    foreign key (customer_id) references customers (customer_id) on update cascade on delete set null,
    foreign key (shop_id) references shops (shop_id) on update cascade on delete set null
);

