# throttles.py
from rest_framework.throttling import UserRateThrottle

class RegisterThrottle(UserRateThrottle):
    rate = '10/minute'
    scope = 'register'

class LoginThrottle(UserRateThrottle):
    rate = '10/minute'

