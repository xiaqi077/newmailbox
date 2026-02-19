# Mailbox Manager

一个现代化的邮箱管理系统，支持多邮箱账号管理、邮件同步、Web界面操作等功能。

## 功能特性

- 📧 **多邮箱支持**：支持 Gmail、Outlook、Yahoo 等主流邮箱服务
- 🔄 **邮件同步**：定时自动同步邮件到本地数据库
- 🌐 **Web 界面**：现代化 Vue.js 前端界面
- 🔐 **安全认证**：JWT 认证机制
- 📊 **邮件管理**：查看、搜索、分类邮件

## 技术栈

- **后端**: Python + FastAPI + SQLAlchemy + SQLite
- **前端**: Vue 3 + TypeScript + Element Plus
- **部署**: Nginx + Systemd

## 快速开始

### 后端启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

## 配置

### 环境变量

创建 `.env` 文件：

```env
DATABASE_URL=sqlite:///./mailbox_v2.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=false
```

## API 文档

启动服务后访问 `http://localhost:8000/docs` 查看交互式 API 文档。

## 部署

参考 `DEPLOY.md` 获取详细的部署指南。

## 许可证

MIT License
