from __future__ import annotations

# dj_auth_rest
from allauth.account.adapter import DefaultAccountAdapter

# Django
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string


class RegisterAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def send_mail(self, template_prefix, email, context):
        if template_prefix == "account/email/email_confirmation_signup":
            template_name = "users/registration/email/email_confirmation_signup.html"
        elif template_prefix == "account/email/email_confirmation_message":
            template_name = "users/registration/email/email_confirmation_message.html"
        else:
            template_name = f"{template_prefix}.html"

        body = render_to_string(template_name, context, self.request).strip()
        to = [email] if isinstance(email, str) else email
        subject = render_to_string(f"{template_prefix}_subject.txt", context)
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)
        from_email = self.get_from_email()
        print(context)
        msg = EmailMessage(subject, body, from_email, to, headers=None)
        msg.send()
