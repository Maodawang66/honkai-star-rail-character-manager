```mermaid
erDiagram

  用户 {
    int user_id PK "用户ID"
    string username "用户名"
    string password "密码"
    string user_type "用户类型"
  }

  阵营 {
    int camp_id PK "阵营ID"
    string camp_name "阵营名称"
  }

  属性 {
    int attribute_id PK "属性ID"
    string attribute_name "属性名称"
  }

  命途 {
    int fate_id PK "命途ID"
    string fate_name "命途名称"
  }

  角色 {
    int character_id PK "角色ID"
    string name "角色名称"
    string description "简介"
    int camp_id FK "阵营ID"
    int attribute_id FK "属性ID"
    int fate_id FK "命途ID"
    string skill "技能"
  }
    玩家_角色 {
    int user_id PK,FK "用户ID"
    int character_id PK,FK "角色ID"
    string star_soul "星魂"
    int level "等级"
    int power "战力"
    string join_time "获得时间"
    int favor "好感度"
  }

  BOSS {
    int boss_id PK "BOSS ID"
    string name "BOSS名称"
    string description "简介"
    int camp_id FK "阵营ID"
    int weakness_id FK "弱点属性ID"
  }

  环境 {
    int env_id PK "环境ID"
    string name "环境名称"
    string buff "环境buff"
  }

  标签 {
    int tag_id PK "标签ID"
    string name "标签名称"
    string tag_type "标签类型"
  }
    角色_标签 {
    int character_id PK,FK "角色ID"
    int tag_id PK,FK "标签ID"
  }

  BOSS_标签 {
    int boss_id PK,FK "BOSS ID"
    int tag_id PK,FK "标签ID"
  }

  环境_标签 {
    int env_id PK,FK "环境ID"
    int tag_id PK,FK "标签ID"
  }

  %% 基数约束
  用户 ||--o{ 玩家_角色 : "1对多"
  角色 ||--o{ 玩家_角色 : "1对多"
  角色 }o--|| 阵营 : "多对一"
  角色 }o--|| 属性 : "多对一"
  角色 }o--|| 命途 : "多对一"
  玩家_角色 }o--|| 用户 : "多对一"
  玩家_角色 }o--|| 角色 : "多对一"

  角色 ||--o{ 角色_标签 : "1对多"
  标签 ||--o{ 角色_标签 : "1对多"

  BOSS }o--|| 阵营 : "多对一"
  BOSS }o--|| 属性 : "弱点属性"
  BOSS ||--o{ BOSS_标签 : "1对多"
  标签 ||--o{ BOSS_标签 : "1对多"

  环境 ||--o{ 环境_标签 : "1对多"
  标签 ||--o{ 环境_标签 : "1对多"