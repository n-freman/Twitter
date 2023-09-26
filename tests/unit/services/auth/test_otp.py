from twitter.services.auth.otp import get_otp, verify_otp


def test_otp_verrification_passes():
    email = 'nazar@gmail.com'
    otp = get_otp(email)
    assert verify_otp(email, otp) is True
