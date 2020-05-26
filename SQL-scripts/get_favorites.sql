CREATE OR REPLACE FUNCTION get_favorites(user_id INTEGER)
RETURNS TABLE ( label_id INT ) AS $$
BEGIN
    RETURN QUERY SELECT fk_label_id FROM "favorite" as f WHERE user_id = f.fk_user_id;
END;
$$ LANGUAGE PLPGSQL;

