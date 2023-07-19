import random

COOKIE_LIST = [
    'wd_guid=544d13f9-f072-4fdc-9989-84452f1ecd52; historyState=state; _bl_uid=XtlO5cqLjv05qpj3t0d0nna8msI4; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1673095377,1673165470,1673257271,1673333037; boss_login_mode=sms; __fid=c58f56b0daac21ec5273e9b4b258f537; wt2=DY4IX_Pe18l5jPqD0AYgnA-G9UnTNtDaZ_zMhCpK7UovHjn5bKxYiZ6NtwTrfsFzsgpxFtIBCopvwd7HdvXTGrg~~; wbg=0; __zp_stoken__=887aefCE3dDAxC0wecFokLmdqeARKZz80V3cWbnglEDsONSs%2FVCMzL295aWdxVWw6Ry4PehcuLyROcX4mdTpZXyFXVEtiREADYGooaVQmYhwcSUtZVAQoNVpLLXZRQkdxBRc9G0QGUFhyNA0%3D; geek_zp_token=V1RN0kEOL031ZiVtRvyB4bLCuw6zrQxCo~; __l=l=%2Fwww.zhipin.com%2Fshanghai%2F&r=&g=&s=3&friend_source=0&s=3&friend_source=0; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1673349533; __c=1673333037; __a=68265253.1672926940.1673257271.1673333037.431.9.106.431'
]


def cookie_dic():
    cookie_string = random.choice(COOKIE_LIST)
    cookie_dict = {}
    for kv in cookie_string.split(';'):
        k = kv.split('=')[0]
        v = kv.split('=')[1]
        cookie_dict[k] = v
    return cookie_dict
