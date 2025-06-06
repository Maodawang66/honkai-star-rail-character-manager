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
- Python 3.9+
- 现代浏览器（Chrome、Firefox、Safari等）

### 安装步骤

1. **克隆项目**
```bash
git clone [你的仓库地址]
cd benkai
```

2. **安装Python依赖**
```bash
cd backend
pip install -r requirements.txt
```

3. **启动后端服务**
```bash
python app.py
```

4. **访问前端**
打开浏览器访问 `frontend/login.html` 开始使用

### 初始数据

系统启动后，你需要：

1. **注册策划账号**（密钥：52648）
2. **添加基础数据**：阵营、属性、命途、标签
3. **创建角色和环境数据**
4. **注册玩家账号**开始体验

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