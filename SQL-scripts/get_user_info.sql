CREATE OR REPLACE FUNCTION get_user_info(iemail VARCHAR)
RETURNS SETOF "user_info" AS $$
BEGIN
    RETURN QUERY SELECT * from "user_info" WHERE email = iemail;
END;
$$ LANGUAGE PLPGSQL;



