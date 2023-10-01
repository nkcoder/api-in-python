create table users
(
    id              serial primary key ,
    user_name       varchar(255)                                             not null unique,
    email           varchar(255)                                             not null
        unique,
    password        varchar(255)                                             not null,
    date_registered timestamp default CURRENT_TIMESTAMP
);

create table orders
(
    id                  serial primary key ,
    buyer_id            integer references users,
    date_placed         timestamp default CURRENT_TIMESTAMP,
    total_amount        numeric(10, 2)                                             not null,
    shipping_address_id integer
);

create table products
(
    id           serial primary key ,
    seller_id    integer references users,
    product_name varchar(255)                                                 not null,
    description  text,
    price        numeric(10, 2)                                               not null,
    quantity     integer                                                      not null
);

create table order_products
(
    id         serial primary key,
    order_id   integer
        references orders
            on delete cascade,
    product_id integer
        references products
            on delete cascade
);