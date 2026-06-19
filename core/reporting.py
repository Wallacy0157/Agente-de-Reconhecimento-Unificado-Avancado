import getpass
import platform
from datetime import datetime
from zoneinfo import ZoneInfo


APP_NAME = "AURA"
APP_VERSION = "v1.0.0"
REPORT_TIMEZONE = "America/Sao_Paulo"
UNKNOWN_VALUE = "Não informado"


def _now():
    try:
        return datetime.now(ZoneInfo(REPORT_TIMEZONE))
    except Exception:
        return datetime.now()


def _first_value(data, keys):
    for key in keys:
        value = data.get(key)
        if value:
            return str(value)
    return UNKNOWN_VALUE


def normalize_user_context(user_context=None):
    if isinstance(user_context, str):
        user_context = {"email": user_context}
    elif not isinstance(user_context, dict):
        user_context = {}

    email = _first_value(user_context, ("email", "e-mail", "mail"))
    username = _first_value(user_context, ("username", "usuario", "user", "login"))

    return {
        "name": _first_value(user_context, ("nome", "name", "full_name", "fullName")),
        "email": email,
        "username": username,
    }


def report_display_user(user_context=None):
    user = normalize_user_context(user_context)
    for key in ("username", "name", "email"):
        if user[key] != UNKNOWN_VALUE:
            return user[key]
    try:
        return getpass.getuser()
    except Exception:
        return UNKNOWN_VALUE


def get_operating_system_label():
    system = platform.system() or UNKNOWN_VALUE
    release = platform.release()
    version = platform.version()
    details = " ".join(part for part in (system, release, version) if part)
    return details or UNKNOWN_VALUE


def build_report_header(user_context=None, generated_at=None):
    generated_at = generated_at or _now()
    user = normalize_user_context(user_context)
    return {
        "software": f"{APP_NAME} {APP_VERSION}",
        "name": user["name"],
        "email": user["email"],
        "username": user["username"],
        "date": generated_at.strftime("%d/%m/%Y"),
        "time": generated_at.strftime("%H:%M:%S"),
        "timezone": REPORT_TIMEZONE,
        "operating_system": get_operating_system_label(),
    }


def format_duration(seconds):
    if seconds is None:
        return UNKNOWN_VALUE
    try:
        seconds = int(round(float(seconds)))
    except (TypeError, ValueError):
        return UNKNOWN_VALUE

    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_report_header_text(title, user_context=None, generated_at=None, duration_seconds=None):
    header = build_report_header(user_context, generated_at)
    lines = [
        "=" * 72,
        title,
        "=" * 72,
        f"Nome do Software e versão: {header['software']}",
        f"Nome: {header['name']}",
        f"E-mail: {header['email']}",
        f"Usuário: {header['username']}",
        f"Data: {header['date']}",
        f"Hora: {header['time']}",
    ]
    if duration_seconds is not None:
        lines.append(f"Tempo de duração: {format_duration(duration_seconds)}")
    lines.extend([
        f"Sistema Operacional: {header['operating_system']}",
        "=" * 72,
        "",
    ])
    return "\n".join(lines)
