from pydantic import BaseModel, field_validator

from ..devices import devices


def validate_device(device, need_connected=True):
    if not device in devices.get_device_list():
        return False, "Invalid Device"

    if not devices.devices.get(device).is_connected and need_connected:
        return False, "Device is not connected"

    return True, {"msg": "success"}


device_list_responses = {
    200: {
        "description": "Success",
        "content": {"application/json": {"example": ["device_01", "device_02"]}},
    }
}


device_responses = {
    200: {
        "description": "Success",
        "content": {"application/json": {"example": {"msg": "success"}}},
    },
    422: {
        "description": "Device Error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_device": {
                        "summary": "Invalid Device",
                        "value": {"detail": "Invalid Device"},
                    },
                    "device_not_connected": {
                        "summary": "Device is not connected",
                        "value": {"detail": "Device is not connected"},
                    },
                }
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {"example": {"detail": "Internal Server Error"}}
        },
    },
}

config_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "READER": "X714",
                    "CONNECTION": "COM5",
                    "PARAMETER": "VALUE",
                }
            }
        },
    },
    422: {
        "description": "Device Error",
        "content": {"application/json": {"example": {"detail": "Invalid Device"}}},
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {"example": {"detail": "Internal Server Error"}}
        },
    },
}

state_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_device": {
                        "summary": "idle",
                        "value": {"state": "idle"},
                    },
                    "device_not_connected": {
                        "summary": "running (reading)",
                        "value": {"state": "running"},
                    },
                }
            }
        },
    },
    422: {
        "description": "Device Error",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_device": {
                        "summary": "Invalid Device",
                        "value": {"detail": "Invalid Device"},
                    },
                    "device_not_connected": {
                        "summary": "Device is not connected",
                        "value": {"detail": "Device is not connected"},
                    },
                }
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {"example": {"detail": "Internal Server Error"}}
        },
    },
}
