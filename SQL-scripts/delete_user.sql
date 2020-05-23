CREATE OR REPLACE PROCEDURE delete_user(iemail VARCHAR)
LANGUAGE PLPGSQL AS $$
BEGIN
    DELETE FROM "user" as u WHERE u.email = iemail;
END;
$$;

