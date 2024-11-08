from .base import *


# Email backend configuration for Gmail
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Use TLS for secure email sending
EMAIL_HOST_USER =  env("EMAIL_HOST_USER") # Your Gmail email address
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")  # Your Gmail password or app-specific password
