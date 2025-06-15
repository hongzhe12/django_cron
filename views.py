import subprocess
import os
import time
from typing import List, Dict, Tuple, Optional
from cron_descriptor import Options, ExpressionDescriptor
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

PRESETS = {
    # 每分钟
    "每分钟执行一次": "* * * * *",
    # 每几分钟
    "每2分钟执行一次": "*/2 * * * *",
    "每3分钟执行一次": "*/3 * * * *",
    "每4分钟执行一次": "*/4 * * * *",
    "每5分钟执行一次": "*/5 * * * *",
    "每10分钟执行一次": "*/10 * * * *",
    "每15分钟执行一次": "*/15 * * * *",
    "每20分钟执行一次": "*/20 * * * *",
    "每30分钟执行一次": "*/30 * * * *",
    # 每小时
    "每小时执行一次": "0 * * * *",
    "每小时的第15分钟执行": "15 * * * *",
    "每小时的第30分钟执行": "30 * * * *",
    "每小时的第45分钟执行": "45 * * * *",
    # 每天
    "每天凌晨执行一次": "0 0 * * *",
    "每天早上6点执行": "0 6 * * *",
    "每天中午12点执行": "0 12 * * *",
    "每天下午6点执行": "0 18 * * *",
    # 每周
    "每周日凌晨执行一次": "0 0 * * 0",
    "每周一凌晨执行一次": "0 0 * * 1",
    "每周二凌晨执行一次": "0 0 * * 2",
    "每周三凌晨执行一次": "0 0 * * 3",
    "每周四凌晨执行一次": "0 0 * * 4",
    "每周五凌晨执行一次": "0 0 * * 5",
    "每周六凌晨执行一次": "0 0 * * 6",
    # 每月
    "每月1号凌晨执行一次": "0 0 1 * *",
    # 每年
    "每年1月1号凌晨执行一次": "0 0 1 1 *"
}

SCRIPT_TYPES = {
    "python": {"ext": ".py", "interpreter": "python"},
    "shell": {"ext": ".sh", "interpreter": "sh"}
}
SCRIPT_DIR = "scripts"

os.makedirs(SCRIPT_DIR, exist_ok=True)


def get_crontab_lines() -> List[str]:
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    context = result.stdout.strip().split("\n")
    context = list(map(lambda x: x.strip(), context))
    if result.returncode == 0 and context != ['']:
        return context
    else:
        return []


def save_crontab(lines: List[str]) -> bool:
    result = subprocess.run(
        ["crontab", "-"],
        input="\n".join(lines) + "\n",
        text=True,
        capture_output=True
    )
    return result.returncode == 0


def create_script(script_type: str, content: str) -> Tuple[str, str]:
    script_name = f"task_{int(time.time() * 1000)}"
    script_ext = SCRIPT_TYPES[script_type]["ext"]
    script_path = os.path.abspath(os.path.join(SCRIPT_DIR, f"{script_name}{script_ext}"))

    normalized_content = content.replace('\r\n', '\n').replace('\r', '\n')
    with open(script_path, "wb") as f:
        f.write(normalized_content.encode('utf-8'))

    if script_type == "shell":
        os.chmod(script_path, 0o755)

    interpreter = SCRIPT_TYPES[script_type]["interpreter"]
    return script_path, f"{interpreter} {script_path}"


def parse_cron_task(task: str) -> Optional[Tuple[str, str]]:
    parts = task.strip().split()
    return " ".join(parts[:5]), " ".join(parts[5:]) if len(parts) >= 6 else None


def get_script_content(script_path: str) -> str:
    try:
        script_path = os.path.abspath(script_path)
        with open(script_path, "r") as f:
            content = f.read()
            return content[content.find("\n") + 1:].strip() if content.startswith("#!") else content.strip()
    except Exception as e:
        print(f"Error reading script: {e}")
        return f"# 无法读取原始脚本\n# 错误: {str(e)}"


def get_preset(schedule: str) -> str:
    inverted_presets = {v: k for k, v in PRESETS.items()}
    return inverted_presets.get(schedule, "")


# 新增 get_log_path 函数
def get_log_path(script_path):
    base_name = os.path.basename(script_path)
    file_name, _ = os.path.splitext(base_name)
    log_dir = os.path.join(os.path.dirname(script_path), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f'{file_name}.log')
    return log_path


def index(request):
    tasks = get_crontab_lines()
    return render(request, 'django_cron/index.html', {'tasks': tasks})


@csrf_exempt
def add(request):
    if request.method == 'POST':
        schedule = request.POST.get('schedule')
        script_type = request.POST.get('script_type')
        script_content = request.POST.get('script_content')

        _, command = create_script(script_type, script_content)
        lines = get_crontab_lines()
        lines.append(f"{schedule} {command}")

        if not save_crontab(lines):
            messages.error(request, "保存crontab失败")
        return redirect('index')

    return render(request, 'django_cron/add.html', {'presets': PRESETS})


@csrf_exempt
def delete(request, task_id):
    lines = get_crontab_lines()
    if 0 <= task_id < len(lines):
        task_info = parse_cron_task(lines[task_id])
        if task_info:
            _, command = task_info
            script_path = command.split()[1]
            try:
                os.remove(script_path)
                # 删除对应的日志文件
                log_path = get_log_path(script_path)
                if os.path.exists(log_path):
                    os.remove(log_path)
            except Exception as e:
                print(f"Error deleting files: {e}")
                messages.error(request, "删除相关文件失败")
        del lines[task_id]
        if not save_crontab(lines):
            messages.error(request, "删除任务失败")
    return redirect('index')


@csrf_exempt
def edit(request, task_id):
    lines = get_crontab_lines()
    if not (0 <= task_id < len(lines)):
        return redirect('index')

    if request.method == 'POST':
        schedule = request.POST.get('schedule')
        script_type = request.POST.get('script_type')
        script_content = request.POST.get('script_content')

        _, command = create_script(script_type, script_content)
        lines[task_id] = f"{schedule} {command}"

        if not save_crontab(lines):
            messages.error(request, "更新任务失败")
        return redirect('index')

    task_info = parse_cron_task(lines[task_id])
    if not task_info:
        messages.error(request, "任务格式无效")
        return redirect('index')

    schedule, command = task_info
    script_type = "python" if command.startswith("python ") else "shell"
    script_path = command[7:] if script_type == "python" else command[3:]
    script_content = get_script_content(script_path)


    return render(request, 'django_cron/edit.html', {
        'presets': PRESETS,
        'schedule': schedule,
        'script_content': script_content,
        'script_type': script_type,
        'selected_preset': get_preset(schedule)
    })


def get_description_route(request):
    cron = request.GET.get('cron', '')
    try:
        options = Options()
        options.locale_code = "zh_CN"
        return HttpResponse(str(ExpressionDescriptor(cron, options)))
    except Exception as e:
        print(f"Error parsing cron expression {cron}: {e}")
        return HttpResponse("无效的 Crontab 表达式")

def view_log(request, log_name):
    """查看日志文件内容"""
    log_paths = [
        "/var/log/cron",
        "/var/log/syslog"
    ]

    log_path = None
    for path in log_paths:
        if os.path.exists(path) and os.path.basename(path) == log_name:
            log_path = path
            break

    if not log_path:
        raise Http404("日志文件不存在")

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = lines[::-1]  # 只取最后 50 行

        paginator = Paginator(lines, 50)  # 每页显示 50 行
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # 优化分页范围，只显示当前页前后各 2 页
        current_page = page_obj.number
        total_pages = paginator.num_pages
        start_page = max(current_page - 2, 1)
        end_page = min(start_page + 4, total_pages)
        if end_page - start_page < 4:
            start_page = max(end_page - 4, 1)

        page_range = range(start_page, end_page + 1)

        content = ''.join(page_obj)
        return render(request, 'django_cron/view_log.html', {
            'log_name': log_name,
            'log_content': content,
            'page_obj': page_obj,
            'page_range': page_range
        })
    except Exception as e:
        raise Http404(f"读取日志文件出错: {str(e)}")

def logs(request):
    """显示日志文件列表"""
    # 定义可能的 crontab 日志文件路径
    log_paths = [
        "/var/log/cron",
        "/var/log/syslog"
    ]

    logs = []
    for log_path in log_paths:
        if os.path.exists(log_path):
            file_size = os.path.getsize(log_path)
            logs.append({
                'name': os.path.basename(log_path),
                'size': file_size
            })

    return render(request, 'django_cron/logs.html', {'logs': logs})