CREATE OR REPLACE FUNCTION create_user(iname VARCHAR, iemail VARCHAR, iphone VARCHAR, istreet VARCHAR, ipassword VARCHAR, izip INTEGER)
RETURNS SETOF "user" AS $$
BEGIN
    RETURN QUERY INSERT INTO "user" (name,email,phone,street,password,fk_zip) VALUES (iname,iemail,iphone,istreet,ipassword,izip) RETURNING *;
END;
$$ LANGUAGE PLPGSQL;

