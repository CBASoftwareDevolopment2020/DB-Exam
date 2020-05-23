CREATE OR REPLACE VIEW user_info AS 
SELECT u.id, u.name, u.email, u.phone, u.street, u.password, r.lon, r.lat, r.zip, r.name as region 
FROM "user" as u 
JOIN "region" as r ON u.fk_zip = r.zip;