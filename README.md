# 崩坏星穹铁道角色管理系统

一个基于Flask后端和原生JavaScript前端的崩坏星穹铁道角色管理系统，支持玩家角色管理、数据查询、智能推荐等功能。

## 🌟 功能特色

### 👥 用户管理
- **双角色系统**：支持玩家和策划两种用户类型
- **安全认证**：策划注册需要专用密钥验证
- **权限控制**：不同用户类型具有不同的功能权限

### 🎮 玩家功能
- **角色管理**：添加、修改、删除个人角色
- **数据查询**：查询角色、BOSS、环境信息
- **战力排行**：查看全服和单角色战力排名
- **持有率统计**：查看角色持有率
- **阵容推荐**：基于BOSS和环境的智能角色推荐
- **抽取推荐**：多维度角色抽取建议

### 🛠️ 策划功能
- **数据维护**：管理角色、BOSS、环境、标签等基础数据
- **智能分析**：AI驱动的新角色设计推荐系统

## 🏗️ 系统架构

```
崩坏星穹铁道角色管理系统/
├── backend/                 # 后端代码
│   ├── app.py              # Flask主应用
│   ├── benkai.db           # SQLite数据库
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   ├── css/               # 样式文件
│   ├── js/                # JavaScript文件
│   ├── *.html            # 页面文件
│   └── images/           # 图片资源
└── docs/                  # 文档
    └── requirements_analysis.tex  # 需求分析文档
```

## 🚀 快速开始

### 环境要求
- **Python 3.9+** 
- **现代浏览器**（Chrome、Firefox、Safari、Edge等）
- **Git**（用于下载和同步项目）

## 📖 新手完整教程

### 第一步：下载项目到本地

1. **安装Git**（如果还没有）
   - Windows：从 [git-scm.com](https://git-scm.com/) 下载安装
   - Mac：`brew install git` 或从App Store安装Xcode
   - Linux：`sudo apt install git` 或 `sudo yum install git`

2. **克隆项目到本地**
```bash
# 打开命令行/终端，运行以下命令
git clone https://github.com/Maodawang66/honkai-star-rail-character-manager.git

# 进入项目目录
cd honkai-star-rail-character-manager
```

### 第二步：配置Python环境

1. **检查Python版本**
```bash
python --version
# 确保版本是3.9或更高
```

2. **安装项目依赖**
```bash
# 进入后端目录
cd backend

# 安装所需的Python库
pip install -r requirements.txt

# 如果pip安装失败，可以尝试：
python -m pip install -r requirements.txt
```

### 第三步：启动系统

1. **启动后端服务器**
```bash
# 在backend目录中运行
python app.py

# 看到以下信息说明启动成功：
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

2. **打开前端页面**
   - 保持后端运行（不要关闭命令行窗口）
   - 用浏览器打开项目中的 `frontend/login.html` 文件
   - 或者直接双击 `login.html` 文件

### 第四步：初始化数据和用户

1. **注册策划账号**（管理员）
   - 点击"注册"
   - 选择用户类型：策划
   - 输入策划密钥：`52648`
   - 填写用户名和密码，完成注册

2. **添加基础数据**（策划用户操作）
   - 登录策划账号
   - 进入"数据维护"页面
   - 按顺序添加：
     - **阵营**：如"仙舟联盟"、"银河议会"等
     - **属性**：如"物理"、"火"、"冰"、"雷"、"风"、"量子"、"虚数"
     - **命途**：如"毁灭"、"巡猎"、"智识"、"同谐"、"虚无"、"存护"、"丰饶"
     - **标签**：如"群攻"、"单体"、"治疗"、"护盾"等

3. **创建角色数据**（策划用户操作）
   - 在角色管理中添加游戏角色
   - 为角色分配阵营、属性、命途
   - 为角色添加相关标签

4. **注册玩家账号**
   - 退出策划账号
   - 注册新用户，选择"玩家"类型
   - 登录玩家账号开始使用

### 第五步：开始使用

**玩家功能**：
- **角色管理**：添加自己拥有的角色，设置等级、星魂、好感度等
- **数据查询**：查看全服角色、BOSS、环境信息
- **阵容推荐**：基于BOSS和环境获取角色推荐
- **抽取推荐**：获得个性化的角色抽取建议

**策划功能**：
- **数据维护**：管理所有基础数据
- **智能推荐**：AI分析推荐新角色设计方案

## 🔄 数据共享教程

### 如何与朋友共享角色数据

#### 情况说明
默认情况下，每个人的角色数据都存储在本地，相互独立。如果想要与朋友共享数据（比如看到彼此的角色收集情况），需要启用数据同步功能。

#### 数据同步步骤

**设置方（第一次配置）**：

1. **确保数据库已同步到Git**
   - 项目已经配置好数据库同步
   - 当前的数据会自动同步到GitHub

2. **上传本地数据**
```bash
# 在项目根目录运行
git add backend/benkai.db
git commit -m "更新角色数据库"
git push
```

**其他用户（获取共享数据）**：

1. **获取最新数据**
```bash
# 在项目根目录运行
git pull
```

2. **重启系统**
   - 关闭后端服务器（Ctrl+C）
   - 重新运行 `python app.py`
   - 刷新浏览器页面

#### 日常数据同步流程

**当有人添加了新的角色数据后**：

1. **数据更新者操作**：
```bash
# 停止后端服务器
# 在项目目录运行：
git add backend/benkai.db
git commit -m "添加了新角色数据"
git push
```

2. **其他人获取更新**：
```bash
# 停止后端服务器
# 在项目目录运行：
git pull
# 重启后端服务器
python backend/app.py
```

#### ⚠️ 数据同步注意事项

**重要规则**：
- 🔄 **一次只能一个人修改数据** - 避免同时添加角色造成冲突
- 📅 **约定更新时间** - 建议每天固定时间统一同步
- 💾 **定期备份** - 重要数据记得备份
- 🔍 **确认再push** - 上传前确保数据正确

**协作建议**：
1. **指定数据管理员** - 一人负责解决可能的冲突
2. **使用群聊协调** - 更新前在群里说一声
3. **分工明确** - 不同人负责不同类型的数据维护

### 故障排除

**常见问题**：

1. **pip安装失败**
```bash
# 尝试升级pip
python -m pip install --upgrade pip
# 或使用conda（如果安装了Anaconda）
conda install flask flask-cors pandas numpy scikit-learn
```

2. **端口占用错误**
   - 关闭其他可能占用5000端口的程序
   - 或修改`app.py`中的端口号

3. **数据库错误**
   - 删除`backend/benkai.db`文件
   - 重新运行`python backend/init_db.py`初始化数据库

4. **Git冲突解决**
```bash
# 如果pull时出现冲突
git stash              # 暂存本地修改
git pull               # 拉取远程更新  
git stash pop          # 恢复本地修改
# 手动解决冲突后重新提交
```

## 📊 核心算法

### 阵容推荐算法
```
角色优先度 = 战力 × (1 + 好感度 × 0.1) × (1 + 匹配标签数 × 0.3)
```

### 智能推荐系统
- **分布分析**：属性-命途组合覆盖度分析
- **机器学习**：随机森林算法预测角色表现
- **综合评估**：多维度角色设计建议

### 抽取推荐策略
1. **缺失标签补充**：推荐能填补标签空白的角色
2. **阵营完整性**：补充缺失阵营角色
3. **属性命途组合**：完善属性-命途矩阵
4. **热门角色**：基于持有率的推荐
5. **个性化预测**：机器学习预测用户喜好

## 🎯 主要页面

- **登录/注册** (`login.html`, `register.html`)
- **玩家主页** (`home.html`)
- **策划主页** (`planner_home.html`)
- **数据查询** (`player_data_query.html`)
- **数据维护** (`data_maintenance.html`)
- **阵容推荐** (`team_recommendation.html`)
- **智能推荐** (`intelligent_recommendation.html`)

## 💾 数据库设计

### 核心实体
- **用户** (User)：用户账号信息
- **角色** (Character)：游戏角色基本信息
- **玩家-角色** (User_Character)：玩家拥有的角色数据
- **BOSS** (Boss)：游戏BOSS信息
- **环境** (Environment)：战斗环境信息
- **标签** (Tag)：多维度标签系统

### 关系设计
- 多对多关系：角色-标签、BOSS-标签、环境-标签
- 外键约束：保证数据一致性
- 索引优化：提升查询性能

## 🔧 技术栈

### 后端
- **框架**：Flask 2.0.1
- **数据库**：SQLite3
- **机器学习**：scikit-learn 1.6.1
- **数据处理**：pandas 2.2.3, numpy 2.0.2
- **跨域支持**：Flask-CORS 3.0.10

### 前端
- **基础**：HTML5, CSS3, JavaScript (ES6+)
- **样式**：原生CSS + 响应式设计
- **交互**：原生JavaScript + Fetch API
- **图标**：Emoji + 自定义样式

## 📈 性能特点

- **轻量级**：无重型框架依赖
- **响应式**：适配不同屏幕尺寸
- **智能化**：AI驱动的推荐算法
- **可扩展**：模块化设计便于功能扩展

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2025-01-XX)
- ✨ 初始版本发布
- 🎮 完整的玩家角色管理系统
- 🛠️ 策划数据维护功能
- 🤖 AI驱动的智能推荐系统
- 📊 多维度数据分析功能

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢所有为崩坏星穹铁道游戏生态贡献的开发者和玩家们！

---

**Made with ❤️ for Honkai: Star Rail players** 