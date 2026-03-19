# AeroVision — 无人机交通智能分析平台

## 一、项目简介

AeroVision 是一个基于 Django 构建的智能网站系统，旨在实现无人机视角下的交通场景分析与管理。

当前阶段主要完成网站基础框架搭建，包括：

- 首页展示（Landing Page）
- 用户注册与登录系统
- 用户个人中心（Dashboard）
- 公告与反馈模块
- 文件上传模块（预留）
- 项目结构与协作规范建立

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
├─ feedback/              # 公告、反馈、联系模块
│
├─ templates/             # HTML 模板
│  ├─ accounts/
│  ├─ dashboard/
│  ├─ uploads/
│  └─ feedback/
│
├─ static/                # 静态资源
│  ├─ css/
│  ├─ js/
│  └─ img/
│
├─ media/                 # 用户上传文件（运行时生成）
├─ docs/                  # 项目文档（结构说明、开发规范等）
│
├─ requirements.txt       # 项目依赖
├─ README.md              # 项目说明
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
负责用户相关功能：
- 用户注册
- 用户登录 / 登出
- 个人信息管理

---

### 3. dashboard
用户登录后的主界面：
- 用户主页
- 功能入口展示
- 后续数据与任务展示

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

## 四、当前开发阶段

当前项目处于 **基础框架搭建阶段**，重点包括：

- 项目结构规范
- 页面基础布局
- 用户系统实现
- 数据库初步设计
- 团队协作流程建立

暂不包含：

- 模型推理功能
- Docker 部署
- 异步任务系统
- 前后端分离架构

---

## 五、运行方式（开发环境）

```bash
pip install -r requirements.txt
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

## 六、Git 协作规范

### 1. 分支规则

- `main`：稳定分支（禁止直接修改）
- `feature/*`：功能开发分支
- `fix/*`：问题修复分支

示例：

```
feature/login
feature/homepage
fix/register-bug
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

| 类型   | 说明           |
|--------|----------------|
| init   | 初始化项目     |
| feat   | 新功能         |
| fix    | 修复问题       |
| style  | 样式调整       |
| docs   | 文档更新       |
| refactor | 重构代码     |

示例：

```
feat: 添加用户登录页面
fix: 修复注册验证问题
docs: 更新项目结构说明
```

---

### 4. 注意事项

- 不要提交 `venv/`
- 不要提交 `db.sqlite3`
- 不要提交 `.env`
- 开发前必须 `git pull`
- 修改数据库结构需提前沟通

---

## 七、后续开发计划

- 完成首页设计（渐变 + 交互）
- 完成用户系统（注册/登录）
- 完成用户 Dashboard 页面
- 实现文件上传功能
- 接入目标检测模型
- 引入 Docker 部署
- 完善系统功能与 UI

---

## 八、项目定位

本项目为：

> 一个结合计算机视觉模型与 Web 系统的智能分析平台

目标是实现：

- 模型能力可视化
- 数据管理系统化
- 用户操作简单化
- 系统结构工程化
