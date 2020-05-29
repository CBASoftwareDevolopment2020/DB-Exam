DROP TABLE IF EXISTS favorite, region, "user";

CREATE TABLE "user" (
    "id" SERIAL PRIMARY KEY,
    "name" varchar NOT NULL,
    "email" varchar UNIQUE NOT NULL,
    "phone" varchar UNIQUE NOT NULL,
    "street" varchar NOT NULL,
    "password" varchar NOT NULL,
    "fk_zip" int NOT NULL
);

CREATE TABLE "region" (
    "zip" int PRIMARY KEY,
    "name" varchar NOT NULL,
    "lat" decimal NOT NULL,
    "lon" decimal NOT NULL
);

CREATE TABLE "favorite" (
    "fk_user_id" int NOT NULL,
    "fk_label_id" int NOT NULL,
    PRIMARY KEY (fk_user_id, fk_label_id)
);

ALTER TABLE "user" ADD FOREIGN KEY("fk_zip") REFERENCES "region" ("zip");
ALTER TABLE "favorite" ADD FOREIGN KEY("fk_user_id") REFERENCES "user" ("id") ON DELETE CASCADE;