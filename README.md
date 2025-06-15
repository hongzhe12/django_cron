# django_cron：Django定时任务管理系统

## 项目简介

`django_cron` 是一个基于Django框架开发的定时任务管理系统，通过Web界面可视化管理crontab任务，支持Python和Shell脚本执行，提供预设时间表达式、任务编辑、日志查看等功能，简化定时任务的创建和维护流程。

## 功能特点

- **可视化任务管理**：通过Web界面添加、编辑、删除定时任务
- **多脚本类型支持**：支持Python和Shell脚本执行
- **预设时间表达式**：内置常用定时规则（每分钟、每小时、每天、每周等）
- **实时日志查看**：支持查看系统crontab日志和任务执行日志
- **表达式解析**：自动将crontab表达式转换为中文描述

## 安装与配置

### 环境要求

- Python 3.6+
- Django 3.2+
- crontab（系统服务）

### 安装步骤

1. **安装依赖包**
```bash
pip install django cron_descriptor
```

2. **添加应用到Django项目**
```python
# settings.py
INSTALLED_APPS = [
    # 其他应用
    'django_cron',
]
```

3. **配置URL路由**
```python
# urls.py
from django.urls import path, include

urlpatterns = [
    # 其他路由
    path('cron/', include('django_cron.urls')),
]
```

4. **创建数据库表**
```bash
python manage.py migrate
```

## 使用指南

### 1. 添加定时任务
1. 访问`/cron/`进入任务列表页，点击"添加任务"
2. 选择预设时间表达式（如"每天凌晨执行一次"）或自定义crontab格式
3. 输入脚本内容（支持Python/Shell），点击"添加任务"

### 2. 管理任务
- **编辑**：点击任务列表中的"编辑"按钮修改时间表达式或脚本内容
- **删除**：点击"删除"按钮移除任务（同时删除脚本和日志文件）

### 3. 查看日志
1. 点击任务列表页"查看日志"按钮
2. 选择日志文件（如`/var/log/cron`）查看任务执行记录

## 项目结构

```
django_cron/
├── admin.py              # 管理后台配置
├── apps.py               # 应用配置
├── models.py             # 数据模型
├── tests.py              # 测试用例
├── urls.py               # URL路由配置
├── views.py              # 视图逻辑
├── scripts/              # 脚本存储目录
│   └── logs/             # 日志存储目录
├── templates/            # 前端模板
│   └── django_cron/
│       ├── add.html      # 添加任务页面
│       ├── edit.html     # 编辑任务页面
│       ├── index.html    # 任务列表页面
│       ├── logs.html     # 日志列表页面
│       └── view_log.html # 日志详情页面
└── test_utils/           # 测试工具
    └── test_app/
        ├── admin.py
        ├── apps.py
        ├── models.py
        └── migrations/
```

## 预设时间表达式

| 描述                | crontab表达式   |
|---------------------|-----------------|
| 每分钟执行一次      | `* * * * *`     |
| 每小时执行一次      | `0 * * * *`     |
| 每天凌晨执行一次    | `0 0 * * *`     |
| 每周一凌晨执行一次  | `0 0 * * 1`     |
| 每月1号凌晨执行一次 | `0 0 1 * *`     |
| 每年1月1号凌晨执行一次 | `0 0 1 1 *`   |

## 日志系统

系统支持两种日志查看方式：
1. **系统日志**：默认读取`/var/log/cron`和`/var/log/syslog`
2. **任务日志**：每个脚本执行时生成对应的`*.log`文件，存储在`scripts/logs/`目录

## 许可证

本项目遵循MIT许可证，详情请查看LICENSE文件。


## cookiecutter 打包配置
```bash
pip uninstall django-cron-manager

cookiecutter https://github.com/hongzhe12/cookiecutter-djangopackage.git

Hongzhe
hongzhe2022@163.com
hongzhe12
Django Cron Manager
django-cron-manager
django_cron
DjangoCronConfig
一个用于管理和调度定时任务的 Django 应用

3.2,4.0,4.1,4.2
1.0.0
Y
1
```

## MANIFEST.in 配置
```bash
include AUTHORS.rst
include CONTRIBUTING.rst
include HISTORY.rst
include LICENSE
include README.rst
include requirements.txt
recursive-include django_cron *.html *.png *.gif *js *.css *jpg *jpeg *svg *py
```


## 编译python软件包
```bash
set PYTHONUTF8=1
python -m build
```

## 安装使用
```bash
pip install dist\django_cron_manager-1.0.0-py2.py3-none-any.whl
```
