from flask import g
class Alert:
    """
    A Class used to raise a visual alert and a feedback message of what raised
    the alert
    """

    def raise_success_alert(message):
        g.message = message
        g.message_color = 'success'
        return

    def raise_danger_alert(message):
        g.message = message
        g.message_color = 'danger'
        return
