user_exists = { 
    'detail': [
        {
            "type":  "user_exists",
            "loc": [
                'body',
                'username',
                'email'
            ],
            'msg': ("User with such "
                "username or email already exists")
        }
    ]
}

user_not_found = {
    'detail': [
        {
            "type": "user_not_found",
            "loc": [
                "body",
                "email"
            ],
            'msg': ("User with such "
                "email not found")
        }
    ]
}

user_already_active= {
    'detail': [
        {
            "type": "user_already_active",
            "loc": [
                "body",
                "email"
            ],
            "msg": ("User with given "
                "email was already activated")
        }
    ]
}

otp_verification_fail = {
    'detail': [
        {
            "type": "otp_verification_fail",
            "loc": [
                "body",
                "otp"
            ],
            "msg": ("Otp could not "
                "be verified")
        }
    ]
}
