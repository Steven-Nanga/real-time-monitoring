CREATE TABLE user_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    activity_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Add some sample data
-- Optional: Add some sample data
INSERT INTO user_activities (user_id, activity_type) VALUES
(1, 'login'),
(1, 'view_product'),
(2, 'purchase'),
(3, 'profile_update'),
(1, 'add_to_cart'),
(4, 'login'),
(1, 'logout'),
(2, 'view_order'),
(3, 'change_password'),
(5, 'sign_up'),
(1, 'view_account');                                              