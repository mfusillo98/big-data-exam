CREATE DATABASE bookizon_books_knowledge_discovery;

USE bookizon_books_knowledge_discovery;
CREATE TABLE time
(
    date_time_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    year         VARCHAR(4)              NOT NULL,
    month        VARCHAR(2)              NOT NULL,
    day          VARCHAR(2)              NOT NULL,
    hour         VARCHAR(2)              NOT NULL,
    minutes      VARCHAR(2)              NOT NULL
);
alter table time add index(year), add index(month), add index(day), add index (hour), add index (minutes);

CREATE TABLE services
(
    service_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name       VARCHAR(255)        NOT NULL
);
alter table services add std_name varchar(255) default null;

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
    lng  VARCHAR(255)
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

