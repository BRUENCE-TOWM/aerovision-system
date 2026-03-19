# AeroVision — 无人机交通智能分析平台

---

## 一、项目简介

AeroVision 是一个基于 Django 构建的智能网站系统，旨在实现无人机视角下的交通场景分析与管理。

本项目当前处于基础开发阶段，重点完成：

- 网站整体框架搭建
- 用户注册与登录系统
- 首页（Landing Page）设计
- 用户个人中心（Dashboard）
- 公告与反馈模块
- 文件上传模块（预留）

后续将逐步接入目标检测模型，实现无人机交通数据的智能分析功能。

---

## 二、项目结构

```text
aerovision/
├─ config/                # Django 项目配置（settings、urls 等）
├─ core/                  # 首页、关于、帮助等公共页面
├─ accounts/              # 用户系统（登录、注册、个人中心）
├─ dashboard/             # 用户登录后的主界面
├─ uploads/               # 上传模块（预留）
├─ feedback/              # 公告、反馈模块
│
├─ templates/             # HTML 模板
│  ├─ accounts/
│  ├─ dashboard/
│  ├─ uploads/
│  └─ feedback/
│
├─ static/                # 静态资源（CSS、JS、图片）
│  ├─ css/
│  ├─ js/
│  └─ img/
│
├─ media/                 # 用户上传文件（运行时生成）
├─ docs/                  # 项目文档（结构说明、开发规范等）
│
├─ requirements.txt       # 项目依赖
├─ README.md              # 项目说明文档
└─ .gitignore             # Git 忽略规则
```

---

## 三、模块说明

### 1. core
负责公共页面：
- 首页（Landing Page）
- 关于页面
- 帮助页面

---

### 2. accounts
负责用户系统：
- 用户注册
- 用户登录 / 登出
- 个人信息管理

---

### 3. dashboard
用户登录后的主界面：
- 用户主页
- 功能入口展示
- 后续任务与数据展示

---

### 4. uploads（预留）
用于后续功能：
- 图片/视频上传
- 数据管理
- 模型输入接口

---

### 5. feedback
用于系统交互：
- 公告发布
- 用户反馈
- 联系信息

---

## 四、开发环境

### Python版本
```
Python 3.10.x
```

---

### 环境管理
使用 Python 自带虚拟环境：

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 安装依赖
```bash
pip install -r requirements.txt
```

---

### 运行项目
```bash
python manage.py migrate
python manage.py runserver
```

访问地址：

```
http://127.0.0.1:8000/
```

后台管理：

```
http://127.0.0.1:8000/admin/
```

---

## 五、环境设计说明（重要）

本项目采用分层环境设计：

### Web系统（当前阶段）
- 使用 `venv` 管理
- 用于 Django 网站开发
- 要求环境稳定、可复现

---

### 模型模块（后续阶段）
- 将独立为单独环境（推荐 conda）
- 用于目标检测 / 深度学习模型
- 避免与 Web 环境产生依赖冲突

---

### 设计原则
> 模型与网站解耦，避免环境污染与依赖冲突

---

## 六、Git 协作规范

### 1. 分支规则

- `main`：稳定分支（禁止直接修改）
- `feature/*`：功能开发分支
- `fix/*`：问题修复分支

示例：

```
feature/login
feature/homepage
feature/dashboard
fix/register-error
```

---

### 2. 开发流程

```bash
git checkout main
git pull origin main

git checkout -b feature/功能名

# 开发完成
git add .
git commit -m "feat: 描述你的功能"
git push origin feature/功能名
```

---

### 3. 提交信息规范

| 类型 | 说明 |
|------|------|
| init | 初始化项目 |
| feat | 新功能 |
| fix | 修复问题 |
| style | 样式调整 |
| docs | 文档更新 |
| refactor | 代码重构 |

示例：

```
feat: 添加用户登录页面
fix: 修复注册验证问题
docs: 更新项目结构说明
```

---

### 4. 注意事项

- ❌ 不要提交 `venv/`
- ❌ 不要提交 `db.sqlite3`
- ❌ 不要提交 `.env`
- ❌ 不要直接修改 `main`
- ✅ 开发前必须 `git pull`
- ✅ 修改数据库结构需提前沟通

---

## 七、当前开发阶段

当前阶段重点：

- 项目结构规范化
- 页面基础搭建
- 用户系统实现
- 团队协作流程建立

暂不包含：

- 模型推理功能
- Docker 部署
- 异步任务系统
- 前后端分离架构

---

## 八、后续开发计划

- 完成首页（渐变 + 动效设计）
- 完成用户注册与登录系统
- 完成 Dashboard 页面
- 实现文件上传功能
- 接入目标检测模型
- 模型与 Web 解耦（API服务）
- 引入 Docker 部署
- 优化 UI 与用户体验

---

## 九、项目定位

本项目为：

> 一个结合计算机视觉模型与 Web 系统的智能分析平台

目标实现：

- 模型能力可视化
- 数据管理系统化
- 用户操作简单化
- 系统结构工程化
