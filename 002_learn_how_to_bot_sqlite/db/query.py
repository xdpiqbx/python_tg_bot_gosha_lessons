def create_table_users():
    return """
        CREATE TABLE IF NOT EXISTS users (
            id INT auto_increment PRIMARY KEY,
            name VARCHAR(50),
            password VARCHAR(65)
        );
    """


def add_new_user():
    return """
        INSERT
            INTO users ('name', 'password')
            VALUES (?, ?);
    """


def select_all_users():
    return """
        SELECT name FROM users;
    """
