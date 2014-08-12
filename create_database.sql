-- host="mysql.server"
-- user="trollsahead"
-- passwd="Test1234"
-- db="trollsahead$clever"

create database if not exists trollsahead$clever;

use trollsahead$clever;

drop table if exists connector;
create table connector (id INT NOT NULL AUTO_INCREMENT,
                        location_key VARCHAR(100) NOT NULL,
                        connector_variant VARCHAR(100) NOT NULL,
                        PRIMARY KEY ( id )
);

drop table if exists downtime;
create table downtime (id INT NOT NULL AUTO_INCREMENT,
                       connector_id INT NOT NULL,
                       timestamp DATE NOT NULL,
                       failure_count INT NOT NULL,
                       PRIMARY KEY ( id ),
                       FOREIGN KEY(connector_id) REFERENCES connector(id)
);

drop table if exists vacancy;
create table vacancy (id INT NOT NULL AUTO_INCREMENT,
                       connector_id INT NOT NULL,
                       timestamp DATE NOT NULL,
                       usage_count INT NOT NULL,
                       PRIMARY KEY ( id ),
                       FOREIGN KEY(connector_id) REFERENCES connector(id)
);

