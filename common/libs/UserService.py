"""
    created by 邱晨 on 2020/5/5 1:08 下午.
"""
import random, string, hashlib, base64


class UserService:

    @staticmethod
    def geneAuth(user_info=None):
        m = hashlib.md5()
        md5_str = '{}-{}-{}-{}-{}'.format(user_info.id, user_info.login_name,
                                          user_info.login_pwd, user_info.login_salt,
                                          user_info.status)
        m.update(md5_str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        md5_str = '{}-{}'.format(base64.encodebytes(pwd.encode('utf-8')), salt)
        m.update(md5_str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        key_list = [random.choice(string.ascii_letters + string.digits)
                for _ in range(length)]
        return ''.join(key_list)



