from database.connection import database_config, cursor

# creating tables function defination
def create_tables():
    # users_table_query = """
    #         CREATE TABLE IF NOT EXISTS USERS(
    #         USERID INT AUTO_INCREMENT,
    #         USERNAME VARCHAR(40),
    #         EMAIL VARCHAR(50) NOT NULL UNIQUE,
    #         PASSWORD VARCHAR(30)
    #         PRIMARY KEY(USERID)
    #     );"""
    users_table_query = """CREATE TABLE IF NOT EXISTS USERS (
            USERID INT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for each user
            USERNAME VARCHAR(40),                        -- Optional username
            EMAIL VARCHAR(50) NOT NULL UNIQUE,           -- Unique email
            PASSWORD VARCHAR(255) NOT NULL          -- Store hashed password, not plain text
        );"""
    cursor.execute(users_table_query)

    notes_table_query = """CREATE TABLE IF NOT EXISTS NOTES (
                        NOTEID INT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for each note
                        USERID INT NOT NULL,                          -- ID of the user who owns the note
                        EMAIL VARCHAR(50) NOT NULL,                     -- Email of the user who owns the note

                        TITLE VARCHAR(100),                          -- Title of the note
                        CONTENT TEXT,                                -- Content of the note
                        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the note was created
                        UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp when the note was last updated
                        FOREIGN KEY (USERID) REFERENCES USERS(USERID) ON DELETE CASCADE  -- Foreign key constraint
                    );"""
    cursor.execute(notes_table_query)
    database_config.commit()
    print("Tables created successfully")