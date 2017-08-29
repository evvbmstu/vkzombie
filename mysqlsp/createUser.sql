CREATE DEFINER=`vv`@`%` PROCEDURE `createUser`(
    IN input_vk         INT,
    IN input_surname    VARCHAR(255),
    IN input_name       VARCHAR(255),
    IN input_uid        VARCHAR(255))
BEGIN
IF ( SELECT exists ( SELECT 1 FROM user WHERE vk_id = input_vk ) )
    THEN UPDATE user SET name    = input_name, 
                         surname = input_surname, 
                         uid     = input_uid WHERE vk_id = input_vk;
ELSE
    INSERT INTO user (
        vk_id,
        surname,
        name,
        signup_date,
        UID )
    VALUES (
        input_vk,
        input_surname,
        input_name,
        NOW(),
        input_uid );
END IF;
END

