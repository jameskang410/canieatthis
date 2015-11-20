-- reset PKs
ALTER TABLE canieatthis.food_table DROP COLUMN row_id;
ALTER TABLE canieatthis.user_table DROP COLUMN row_id;
ALTER TABLE canieatthis.food_table ADD COLUMN row_id serial NOT NULL PRIMARY KEY;
ALTER TABLE canieatthis.user_table ADD COLUMN row_id serial NOT NULL PRIMARY KEY;