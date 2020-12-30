import requests
import json
from django.core.mail import EmailMultiAlternatives

from delivery.settings import SENDGRID_AUTH_TOKEN
from delivery.settings import SENDGRID_URL
from delivery.settings import SENDGRID_EMAIL


def send_email(message, subject, to):

    auth_token = SENDGRID_AUTH_TOKEN

    url = SENDGRID_URL

    header = {
        'Authorization': 'Bearer ' + auth_token
    }

    data = {
        "personalizations": [
            {"to":
                [
                    {
                        "email": to
                    }
                ]
            }
        ],
        "from": {
            "email": SENDGRID_EMAIL
        },
        "subject": subject,
        "content": [
            {"type": "text/html", "value": message}
        ]
    }

    response = requests.post(url, json=data, headers=header)

    print(response)

    return