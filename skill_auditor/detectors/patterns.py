"""
危险模式定义

基于三大战神讨论整合的 25+ 危险模式检测规则
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Pattern


class Severity(Enum):
    """风险严重程度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Category(Enum):
    """风险类别"""
    DESTRUCTIVE = "破坏性操作"
    REMOTE_EXEC = "远程执行"
    CMD_INJECTION = "命令注入"
    NETWORK = "网络外传"
    PRIVILEGE = "权限提升"
    SECRETS = "敏感泄露"
    PERSISTENCE = "持久化"


@dataclass
class PatternRule:
    """危险模式规则"""
    id: str
    name: str
    pattern: Pattern
    severity: Severity
    category: Category
    weight: int
    description: str
    hard_trigger: bool = False


# 危险模式规则库
PATTERN_RULES: List[PatternRule] = [
    # A. 破坏性操作
    PatternRule(
        id="RM_RF_ROOT", name="删除根目录",
        pattern=re.compile(r'rm\s+(-[a-zA-Z]*)*\s*-r[a-zA-Z]*\s+(-[a-zA-Z]*\s+)*[/]($|\s|;|\|)', re.I),
        severity=Severity.CRITICAL, category=Category.DESTRUCTIVE,
        weight=100, description="rm -rf / 删除根目录", hard_trigger=True
    ),
    PatternRule(
        id="RM_RF_HOME", name="删除用户目录",
        pattern=re.compile(r'rm\s+(-[a-zA-Z]*)*\s*-r[a-zA-Z]*\s+(-[a-zA-Z]*\s+)*(~|\$HOME)', re.I),
        severity=Severity.CRITICAL, category=Category.DESTRUCTIVE,
        weight=90, description="rm -rf ~ 删除用户目录", hard_trigger=True
    ),
    PatternRule(
        id="DD_WIPE", name="磁盘擦除",
        pattern=re.compile(r'dd\s+.*of=/dev/(sd[a-z]|nvme|hd[a-z]|vd[a-z])', re.I),
        severity=Severity.CRITICAL, category=Category.DESTRUCTIVE,
        weight=100, description="dd 写入磁盘设备", hard_trigger=True
    ),
    PatternRule(
        id="MKFS_FORMAT", name="格式化磁盘",
        pattern=re.compile(r'mkfs(\.[a-z0-9]+)?\s+/dev/', re.I),
        severity=Severity.CRITICAL, category=Category.DESTRUCTIVE,
        weight=100, description="mkfs 格式化命令", hard_trigger=True
    ),

    # B. 远程执行
    PatternRule(
        id="CURL_PIPE_SH", name="Curl管道执行",
        pattern=re.compile(r'curl\s+[^|]*\|\s*(ba)?sh', re.I),
        severity=Severity.CRITICAL, category=Category.REMOTE_EXEC,
        weight=90, description="curl | sh 远程执行", hard_trigger=True
    ),
    PatternRule(
        id="WGET_PIPE_SH", name="Wget管道执行",
        pattern=re.compile(r'wget\s+[^|]*\|\s*(ba)?sh', re.I),
        severity=Severity.CRITICAL, category=Category.REMOTE_EXEC,
        weight=90, description="wget | sh 远程执行", hard_trigger=True
    ),
    PatternRule(
        id="BASE64_EXEC", name="Base64解码执行",
        pattern=re.compile(r'base64\s+(-d|--decode)[^|]*\|\s*(ba)?sh', re.I),
        severity=Severity.CRITICAL, category=Category.REMOTE_EXEC,
        weight=85, description="base64 解码后执行", hard_trigger=True
    ),

    # C. 命令注入
    PatternRule(
        id="PY_EVAL", name="Python eval",
        pattern=re.compile(r'\beval\s*\('),
        severity=Severity.HIGH, category=Category.CMD_INJECTION,
        weight=70, description="eval() 动态执行"
    ),
    PatternRule(
        id="PY_EXEC", name="Python exec",
        pattern=re.compile(r'\bexec\s*\('),
        severity=Severity.HIGH, category=Category.CMD_INJECTION,
        weight=70, description="exec() 动态执行"
    ),
    PatternRule(
        id="OS_SYSTEM", name="os.system",
        pattern=re.compile(r'os\.system\s*\('),
        severity=Severity.HIGH, category=Category.CMD_INJECTION,
        weight=65, description="os.system() Shell执行"
    ),
    PatternRule(
        id="SUBPROCESS_SHELL", name="subprocess shell=True",
        pattern=re.compile(r'subprocess\.(run|call|Popen)\s*\([^)]*shell\s*=\s*True', re.DOTALL),
        severity=Severity.HIGH, category=Category.CMD_INJECTION,
        weight=65, description="subprocess shell=True"
    ),

    # D. 网络外传
    PatternRule(
        id="CURL_POST", name="Curl POST",
        pattern=re.compile(r'curl\s+[^;|]*-X\s*POST', re.I),
        severity=Severity.MEDIUM, category=Category.NETWORK,
        weight=40, description="curl POST 请求"
    ),
    PatternRule(
        id="NETCAT", name="Netcat连接",
        pattern=re.compile(r'\bnc\s+(-[a-z]*\s+)*[a-zA-Z0-9.-]+\s+\d+', re.I),
        severity=Severity.HIGH, category=Category.NETWORK,
        weight=60, description="netcat 网络连接"
    ),
    PatternRule(
        id="PY_URLLIB", name="Python urllib",
        pattern=re.compile(r'urllib\.request\.urlopen\s*\('),
        severity=Severity.MEDIUM, category=Category.NETWORK,
        weight=35, description="urllib 网络请求"
    ),

    # E. 权限提升
    PatternRule(
        id="SUDO", name="sudo提权",
        pattern=re.compile(r'\bsudo\s+'),
        severity=Severity.HIGH, category=Category.PRIVILEGE,
        weight=60, description="sudo 权限提升"
    ),
    PatternRule(
        id="CHMOD_777", name="chmod 777",
        pattern=re.compile(r'chmod\s+(-[a-zA-Z]*\s+)*7[0-7]{2}'),
        severity=Severity.HIGH, category=Category.PRIVILEGE,
        weight=55, description="chmod 777 开放权限"
    ),
    PatternRule(
        id="SUDOERS", name="sudoers修改",
        pattern=re.compile(r'(/etc/sudoers|visudo|NOPASSWD)', re.I),
        severity=Severity.CRITICAL, category=Category.PRIVILEGE,
        weight=95, description="sudoers 文件修改", hard_trigger=True
    ),

    # F. 持久化
    PatternRule(
        id="CRONTAB", name="Crontab持久化",
        pattern=re.compile(r'(crontab\s+-|/etc/cron)', re.I),
        severity=Severity.HIGH, category=Category.PERSISTENCE,
        weight=65, description="crontab 持久化"
    ),
    PatternRule(
        id="SSH_KEYS", name="SSH密钥注入",
        pattern=re.compile(r'(>>|>)\s*~?/?(\.ssh/authorized_keys|\.ssh/id_)', re.I),
        severity=Severity.CRITICAL, category=Category.PERSISTENCE,
        weight=90, description="SSH 密钥写入", hard_trigger=True
    ),

    # G. 敏感泄露
    PatternRule(
        id="PRIVATE_KEY", name="私钥硬编码",
        pattern=re.compile(r'-----BEGIN\s+(RSA|OPENSSH|EC|DSA)?\s*PRIVATE KEY-----', re.I),
        severity=Severity.CRITICAL, category=Category.SECRETS,
        weight=85, description="硬编码私钥", hard_trigger=True
    ),
    PatternRule(
        id="API_KEY", name="API Key",
        pattern=re.compile(r'(api[_-]?key|apikey|api_secret)\s*[=:]\s*["\'][a-zA-Z0-9_-]{16,}["\']', re.I),
        severity=Severity.HIGH, category=Category.SECRETS,
        weight=60, description="硬编码 API Key"
    ),
    PatternRule(
        id="PASSWORD", name="密码硬编码",
        pattern=re.compile(r'(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{4,}["\']', re.I),
        severity=Severity.HIGH, category=Category.SECRETS,
        weight=55, description="硬编码密码"
    ),
    PatternRule(
        id="AWS_KEY", name="AWS密钥",
        pattern=re.compile(r'(AKIA|ASIA)[A-Z0-9]{16}'),
        severity=Severity.CRITICAL, category=Category.SECRETS,
        weight=80, description="AWS Access Key"
    ),
    PatternRule(
        id="GITHUB_TOKEN", name="GitHub Token",
        pattern=re.compile(r'ghp_[a-zA-Z0-9]{36}'),
        severity=Severity.CRITICAL, category=Category.SECRETS,
        weight=80, description="GitHub Token"
    ),
]


def get_all_patterns() -> List[PatternRule]:
    return PATTERN_RULES


def get_hard_triggers() -> List[PatternRule]:
    return [p for p in PATTERN_RULES if p.hard_trigger]
