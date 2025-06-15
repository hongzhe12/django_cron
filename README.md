
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
