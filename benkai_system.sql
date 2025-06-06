-- 创建用户表
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    user_type TEXT NOT NULL
);

-- 创建阵营表
CREATE TABLE Camp (
    camp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    camp_name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建属性表
CREATE TABLE Attribute (
    attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,
    attribute_name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建命途表
CREATE TABLE Fate (
    fate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fate_name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建角色表
CREATE TABLE Character (
    character_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    camp_id INT,
    attribute_id INT,
    fate_id INT,
    skill TEXT,
    FOREIGN KEY (camp_id) REFERENCES Camp(camp_id),
    FOREIGN KEY (attribute_id) REFERENCES Attribute(attribute_id),
    FOREIGN KEY (fate_id) REFERENCES Fate(fate_id)
);

-- 创建玩家-角色表
CREATE TABLE User_Character (
    user_id INT,
    character_id INT,
    star_soul INT DEFAULT 0,
    level INT DEFAULT 1,
    power INT DEFAULT 0,
    join_time DATETIME,
    favor INT DEFAULT 0,
    PRIMARY KEY (user_id, character_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (character_id) REFERENCES Character(character_id)
);

-- 创建BOSS表
CREATE TABLE Boss (
    boss_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    camp_id INT,
    weakness_id INT,
    FOREIGN KEY (camp_id) REFERENCES Camp(camp_id),
    FOREIGN KEY (weakness_id) REFERENCES Attribute(attribute_id)
);

-- 创建环境表
CREATE TABLE Environment (
    env_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    buff TEXT
);

-- 创建标签表
CREATE TABLE Tag (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建角色-标签关联表
CREATE TABLE Character_Tag (
    character_id INT,
    tag_id INT,
    PRIMARY KEY (character_id, tag_id),
    FOREIGN KEY (character_id) REFERENCES Character(character_id),
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);

-- 创建BOSS-标签关联表
CREATE TABLE Boss_Tag (
    boss_id INT,
    tag_id INT,
    PRIMARY KEY (boss_id, tag_id),
    FOREIGN KEY (boss_id) REFERENCES Boss(boss_id),
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);

-- 创建环境-标签关联表
CREATE TABLE Environment_Tag (
    env_id INT,
    tag_id INT,
    PRIMARY KEY (env_id, tag_id),
    FOREIGN KEY (env_id) REFERENCES Environment(env_id),
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);