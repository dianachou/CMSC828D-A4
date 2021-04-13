/* Create Schema and Table for A2 */
CREATE SCHEMA a2;
CREATE TABLE a2.shootings(
  id                        INT PRIMARY KEY,
  name                      VARCHAR (40),
  date                      DATE,
  manner_of_death           VARCHAR (20),
  armed                     VARCHAR (40),
  age                       INT,
  gender                    CHAR (1),
  race                      VARCHAR (10),
  city                      VARCHAR (40),
  state                     CHAR (2),
  signs_of_mental_illness   BOOLEAN,
  threat_level              VARCHAR (15),
  flee                      VARCHAR (15),
  body_camera               BOOLEAN,
  arms_category             VARCHAR (30),
  age_group                 VARCHAR (20)
);

/* Create Schema and Table for A3. The table is  */
CREATE SCHEMA a3;
CREATE TABLE a3.shootings(
  id                        INT PRIMARY KEY,
  name                      VARCHAR (40),
  date                      DATE,
  manner_of_death           VARCHAR (20),
  armed                     VARCHAR (40),
  age                       INT,
  gender                    CHAR (1),
  race                      VARCHAR (10),
  city                      VARCHAR (40),
  state                     CHAR (2),
  signs_of_mental_illness   BOOLEAN,
  threat_level              VARCHAR (15),
  flee                      VARCHAR (15),
  body_camera               BOOLEAN,
  arms_category             VARCHAR (30),
  age_group                 VARCHAR (20)
);

/* GRANT Permissions */
GRANT CONNECT ON DATABASE a3database TO cmsc828d;
GRANT ALL PRIVILEGES ON DATABASE a3database TO cmsc828d;

/* A2 Permissions */
GRANT USAGE ON SCHEMA a2 TO cmsc828d;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA a2 TO cmsc828d;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA a2 TO cmsc828d;

/* A3 Permissions */
GRANT USAGE ON SCHEMA a3 TO cmsc828d;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA a3 TO cmsc828d;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA a3 TO cmsc828d;
