DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS datasets;

CREATE TABLE users (
    user_id CHAR(36) PRIMARY KEY,
    username TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE datasets (
    dataset_id CHAR(36) PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    author_id CHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tablename TEXT NOT NULL,

    data_field TEXT NOT NULL,
    data_field_type TEXT NOT NULL,
    label_field TEXT NOT NULL,
    label_field_type TEXT NOT NULL,
    user_based_labeling BOOLEAN NOT NULL,

    allow_modify_data BOOLEAN NOT NULL,
    allow_upsert_data BOOLEAN NOT NULL,
    allow_delete_data BOOLEAN NOT NULL,

    FOREIGN KEY (author_id) REFERENCES users (user_id)
);

CREATE TABLE assignments (
    assignment_id CHAR(36) PRIMARY KEY NOT NULL,
    assigner_id CHAR(36) NOT NULL,
    assignee_id CHAR(36) NOT NULL,
    dataset_id CHAR(36) NOT NULL,
    assignment TEXT NOT NULL,

    FOREIGN KEY (assigner_id) REFERENCES users (user_id),
    FOREIGN KEY (assignee_id) REFERENCES users (user_id),
    FOREIGN KEY (dataset_id) REFERENCES datasets (dataset_id)
)

-- CREATE TRIGGER AutoGenerateUserGUID
-- AFTER INSERT ON tblUsers
-- FOR EACH ROW
-- WHEN (NEW.user_id IS NULL)
-- BEGIN
--    UPDATE users SET user_id = (select hex( randomblob(4)) || '-' || hex( randomblob(2))
--              || '-' || '4' || substr( hex( randomblob(2)), 2) || '-'
--              || substr('AB89', 1 + (abs(random()) % 4) , 1)  ||
--              substr(hex(randomblob(2)), 2) || '-' || hex(randomblob(6)) ) WHERE rowid = NEW.rowid;
-- END;