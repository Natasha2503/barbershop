-- Database: barbershop
DROP table IF EXISTS clientsbarber;
DROP table IF EXISTS masters;
DROP table IF EXISTS name_of_clients;
DROP table IF EXISTS number_telephone;


CREATE DOMAIN name_of_clients AS TEXT
CHECK(
   VALUE ~ '[a-zA-Zа-яА-я]'
);

create domain number_telephone as TEXT
check(
	value ~ '\d+'
);


create table masters (
	id SERIAL PRIMARY KEY NOT NULL,
	name varchar(50) not null
);

CREATE TABLE clientsbarber (
    id SERIAL PRIMARY KEY NOT NULL,
    nameclient name_of_clients not null,
    telephone number_telephone not null,
	date_of_record timestamp not null,
    id_master integer not null,
	FOREIGN KEY (id_master) REFERENCES masters (id)
);