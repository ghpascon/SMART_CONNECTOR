class FastAlerts:
    def __init__(self):
        self.alerts: list[dict] = []

    def add_alert(self, detail: str, style: str = 'alert-primary'):
        """
        Add an alert message with a specified Bootstrap style.
        Parameters:
        - detail (str): The message content to display.
        - style (str): Bootstrap alert style. One of the following:
            - 'alert-primary'   (default blue)
            - 'alert-secondary' (neutral gray)
            - 'alert-success'   (green for success)
            - 'alert-danger'    (red for errors)
            - 'alert-warning'   (yellow for warnings)
            - 'alert-info'      (light blue for information)
            - 'alert-light'     (light background)
            - 'alert-dark'      (dark background)
        """
        self.alerts.append({
            "detail": detail,
            "style": style
        })

    def get_alerts(self) -> list[dict]:
        """
        Return all current alerts and clear the list.

        Returns:
        - list[dict]: A list of dictionaries with 'detail' and 'style' keys.
        """
        alerts = self.alerts
        self.clear_alerts()
        return alerts

    def clear_alerts(self):
        """
        Clear all stored alerts.
        """
        self.alerts = []

fast_alerts = FastAlerts()