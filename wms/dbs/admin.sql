INSERT INTO users (username, password)
VALUES ('admin', 'pbkdf2:sha256:150000$KhvBcw1b$c685f95e4e3cffba1ef64146a1df3fc176d20b63a86afd5c97dc3810db708848');
INSERT INTO roles (name, description)
VALUES ('admin', 'Admin role');
INSERT INTO users_roles (user_id, role_id)
VALUES (1, 1);