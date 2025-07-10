from datetime import datetime

from fastapi.templating import Jinja2Templates

from .path import get_path
from ..schemas.devices import devices
from .fast_alerts import fast_alerts


def generate_footer():
    year = datetime.now().year
    return f"© {year} - SMARTX"


templates = Jinja2Templates(directory=get_path("app/templates"))
templates.env.globals["generate_footer"] = generate_footer
templates.env.globals["device_list"] = devices.get_device_list
templates.env.globals["is_rfid_reader"] = devices.is_rfid_reader
templates.env.globals["get_alerts"] = fast_alerts.get_alerts
