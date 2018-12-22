# 导他妈的
from __future__ import unicode_literals
from collections import OrderedDict

try:
    from alienVan.appConfig import *

except ImportError:
    from alienVan.appConfig import *

import onedrivesdk
from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest
from os.path import splitext


# 初始化
# 非商业版(个人版)
def init_N(code=None):
    '''
    用于普通版的oneDrive，office365商业版无法使用的初始化函数。
    用户登录，获取详细信息，将详细信息保存在conf文件中。
    在第一次登录时使用。
    :param client:
    :return:
    '''
    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider = http_provider,
        client_id = client_id_normal,
        scopes = scopes)

    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

    # 有code码时返回client对象，无则发射授权登陆URL
    if code:
        client.auth_provider.authenticate(code, redirect_uri, client_secret_normal)
        # 保存session()
        auth_provider.save_session()
        return client
    else:
        auth_url = client.auth_provider.get_auth_url(redirect_uri)
        return auth_url

def init_B(code=None):
    '''
    备用
    用于登陆Business/Office 365版OneDrive的初始化函数。
    用户登录，获取详细信息，将详细信息保存在conf文件中。
    在第一次登录时使用。
    Ref:
    https://github.com/OneDrive/onedrive-sdk-python#onedrive-for-business
    https://dev.onedrive.com/auth/aad_oauth.htm#register-your-app-with-azure-active-directory
    :param client:
    :return:
    '''
    # auth url:
    # https://login.microsoftonline.com/common/oauth2/authorize?scope=wl.signin+wl.offline_access+onedrive.readwrite&redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=bac72a8b-77c8-4b76-8b8f-b7c65a239ce6

    http = onedrivesdk.HttpProvider()
    auth = onedrivesdk.AuthProvider(
        http_provider = http,
        client_id = client_id_business,
        auth_server_url = auth_server_url,
        auth_token_url = auth_token_url)
    auth_url = auth.get_auth_url(redirect_uri)

    # now the url looks like "('https://login.microsoftonline.com/common/oauth2/authorize',)?redirect_uri=https%3A%2F%2Fod.cnbeining.com&response_type=code&client_id=bac72a8b-77c8-4b76-8b8f-b7c65a239ce6"

    if code:
        try:  # Python 2
            auth_url = auth_url.encode('utf-8').replace("('", '').replace("',)", '')
        except TypeError:
            auth_url = auth_url.replace("('", '').replace("',)", '')

        return auth_url
    else:
        auth.authenticate(code, redirect_uri, client_secret_business, resource = 'https://api.office.com/discovery/')

        # this step is slow
        service_info = ResourceDiscoveryRequest().get_service_info(auth.access_token)[0]

        auth.redeem_refresh_token(service_info.service_resource_id)

        client = onedrivesdk.OneDriveClient(service_info.service_resource_id + '_api/v2.0/', auth, http)


        return client

# 其他工具
# def authUrlToClient(funcName):

def getClient(funcName):
    if funcName == 'N':
        return init_N()
    else:
        return init_B()

if __name__ == '__main__':
    #todo 测试登陆授权并且保存session,并读取session
    print(init_N())
    code = input('code:')
    client = init_N(code)
    print(client)
    print('保存一下session')
    from odTools.session import save_session,load_session
    save_session(client, '888.json')
    print('不出意外的话，保存完毕')
    '''
    报错
        Traceback (most recent call last):
      File "/home/rq/softwares/pycharm-2018.2.4/helpers/pydev/pydevd.py", line 1664, in <module>
        main()
      File "/home/rq/softwares/pycharm-2018.2.4/helpers/pydev/pydevd.py", line 1658, in main
        globals = debugger.run(setup['file'], None, None, is_module)
      File "/home/rq/softwares/pycharm-2018.2.4/helpers/pydev/pydevd.py", line 1068, in run
        pydev_imports.execfile(file, globals, locals)  # execute the script
      File "/home/rq/softwares/pycharm-2018.2.4/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
        exec(compile(contents+"\n", file, 'exec'), glob, loc)
      File "/home/rq/workspace/python/AlienVan/odTools/authentication.py", line 112, in <module>
        client = load_session(client, i)
      File "/home/rq/workspace/python/AlienVan/odTools/session.py", line 101, in load_session
        status_dict = json.loads(session_file.read())
      File "/usr/lib/python3.6/json/__init__.py", line 354, in loads
        return _default_decoder.decode(s)
      File "/usr/lib/python3.6/json/decoder.py", line 339, in decode
        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
      File "/usr/lib/python3.6/json/decoder.py", line 357, in raw_decode
        raise JSONDecodeError("Expecting value", s, err.value) from None
    json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    '''
    #todo 待解决json读取报错，且删除session保存pockle的操作
    from odTools.otherHandler import fileList
    from alienVan.settings import BASE_DIR
    fl = fileList(BASE_DIR,'.json')
    for i in fl:
        client = load_session(client, i)
        print(client)