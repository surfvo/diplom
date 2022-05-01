DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS parking_place CASCADE;

create table users
(
    tg_id        double precision not null
        constraint users_pk
            primary key,
    name         varchar,
    is_admin     boolean,
    last_message integer
);


create unique index  users_tg_id_uindex
    on users (tg_id);


create table parking_place
(
    id             serial
        constraint parking_place_pk
            primary key,
    verified       boolean,
    address        varchar,
    parking_number varchar,
    img_link_1     varchar,
    img_link_2     varchar,
    img_link_3     varchar,
    verify_img     varchar,
    price_day      real,
    price_week     real,
    price_month    real,
    date_start     timestamp,
    phone          real,
    comment        varchar,
    owner_id       double precision,
    date_end       timestamp
);

create unique index parking_place_id_uindex
    on parking_place (id);


