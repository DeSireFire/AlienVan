import requests
import json
import subprocess
import os
import time
import base64
import sys
if sys.version_info[0]==2:
    import xmlrpclib
else:
    import xmlrpc.client as xmlrpclib


class PyAria2(object):

    def __init__(self,host,port,secret,scheme,session=None):
        '''
        PyAria2构造函数。
        host：字符串，aria2 rpc主机，默认为'localhost'
        端口：整数，aria2 rpc端口，默认为6800
        会话：字符串，aria2 rpc会话保存。
        '''
        if not isAria2Installed():
            raise Exception('aria2 尚未安装，请先安装aria2')

        if not isAria2rpcRunning():
            cmd = 'aria2c' \
                  ' --enable-rpc' \
                  ' --rpc-listen-port {}' \
                  ' --continue' \
                  ' --max-concurrent-downloads=20' \
                  ' --max-connection-per-server=10' \
                  ' --rpc-max-request-size=1024M'.format(port)

            if not session is None:
                cmd += ' --input-file=%s' \
                       ' --save-session-interval=60' \
                       ' --save-session=%s' % (session, session)

            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            count = 0
            while True:
                if isAria2rpcRunning():
                    break
                else:
                    count += 1
                    time.sleep(3)
                if count == 5:
                    raise Exception('aria2 RPC server started failure.')
            print('aria2 RPC server is started.')
        else:
            print('aria2 RPC server is already running.')
        self.server_uri = scheme+'://{}:{}/jsonrpc'.format(host, port)
        self.secret = secret
        self.server = xmlrpclib.ServerProxy(self.server_uri, allow_none=True)

    def sendJsonRPC(self, data):
        r = requests.post(self.server_uri, data=data)
        return r.text

    def getRPCBody(self, method, params=None):
        '''Create RPC body'''
        uid = '1'
        params = params if params else []
        if self.secret is not None and self.secret!='':
            params.insert(0, 'token:{}'.format(self.secret))
        j = json.dumps([{
            'jsonrpc': '2.0',
            'id': uid,
            'method': method,
            'params': params,
        }])
        return j

    def addUri(self, uris, options=None, position=None):
        '''
        此方法添加了新的HTTP（S）/ FTP / BitTorrent磁体URI。
        uris：列表，URI列表
        选项：dict，其他选项
        position：整数，在下载队列中的位置
        返回：此方法返回注册下载的GID。
        '''
        params = [[uris]]
        if options:
            params.append(options)
        #params.append(position)
        return self.sendJsonRPC(data=self.getRPCBody('aria2.addUri', params))

    def addTorrent(self, torrent, uris=None, options=None, position=None):
        '''
        此方法通过上传“ .torrent”文件来添加BitTorrent下载。
        torrent：字符串，torrent文件路径
        uris：列表，网络种子URI的列表
        选项：dict，其他选项
        position：整数，在下载队列中的位置
        返回：此方法返回注册下载的GID。
        '''
        return self.server.aria2.addTorrent(xmlrpclib.Binary(open(torrent, 'rb').read()), uris, options, position)

    def addMetalink(self, metalink, options=None, position=None):
        '''
        此方法通过上传“ .metalink”文件来添加Metalink下载。
        metalink：字符串，metalink文件路径
        选项：dict，其他选项
        position：整数，在下载队列中的位置
        返回：此方法返回已注册下载的GID列表。
        '''
        return self.server.aria2.addMetalink(xmlrpclib.Binary(open(metalink, 'rb').read()), options, position)

    def remove(self, gid):
        '''
        此方法删除了gid表示的下载。
        gid：字符串，GID。
        返回：此方法返回已删除下载的GID。
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.remove', params))


    def forceRemove(self, gid):
        '''
        此方法删除了gid表示的下载。
        gid：字符串，GID。
        返回：此方法返回已删除下载的GID。
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.forceRemove', params))

    def pause(self, gid):
        '''
        此方法暂停gid表示的下载。
        gid：字符串，GID。
        返回：此方法返回已暂停下载的GID。
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.pause', params))

    def pauseAll(self):
        '''
        This method is equal to calling aria2.pause() for every active/waiting download.
        return: This method returns OK for success.
        此方法等于对每个活动/正在等待的下载都调用aria2.pause（）。
        返回值：此方法成功返回OK。
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.pauseAll'))

    def forcePause(self, gid):
        '''
        This method pauses the download denoted by gid.
        gid: string, GID.
        return: This method returns GID of paused download.
        此方法暂停gid表示的下载。
        gid：字符串，GID。
        返回：此方法返回已暂停下载的GID。
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.forcePause', params))

    def forcePauseAll(self):
        '''
        This method is equal to calling aria2.forcePause() for every active/waiting download.
        return: This method returns OK for success.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.forcePauseAll'))

    def unpause(self, gid):
        '''
        This method changes the status of the download denoted by gid from paused to waiting.
        gid: string, GID.
        return: This method returns GID of unpaused download.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.unpause', params))

    def unpauseAll(self):
        '''
        This method is equal to calling aria2.unpause() for every active/waiting download.
        return: This method returns OK for success.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.unpauseAll'))

    def tellStatus(self, gid, keys=None):
        '''
        This method returns download progress of the download denoted by gid.
        gid: string, GID.
        keys: list, keys for method response.
        return: The method response is of type dict and it contains following keys.
        '''
        params = [gid]
        if keys:
            params.append(keys)
        return self.sendJsonRPC(data=self.getRPCBody('aria2.tellStatus', params))


    def getUris(self, gid):
        '''
        This method returns URIs used in the download denoted by gid.
        gid: string, GID.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getUris', params))

    def getFiles(self, gid):
        '''
        This method returns file list of the download denoted by gid.
        gid: string, GID.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getFiles', params))


    def getPeers(self, gid):
        '''
        This method returns peer list of the download denoted by gid.
        gid: string, GID.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        return self.server.aria2.getPeers(gid)

    def getServers(self, gid):
        '''
        This method returns currently connected HTTP(S)/FTP servers of the download denoted by gid.
        gid: string, GID.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        return self.server.aria2.getServers(gid)

    def tellActive(self, keys=None):
        '''
        This method returns the list of active downloads.
        keys: keys for method response.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        return self.server.aria2.tellActive(keys)

    def tellWaiting(self, offset, num, keys=None):
        '''
        This method returns the list of waiting download, including paused downloads.
        offset: integer, the offset from the download waiting at the front.
        num: integer, the number of downloads to be returned.
        keys: keys for method response.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        return self.server.aria2.tellWaiting(offset, num, keys)

    def tellStopped(self, offset, num, keys=None):
        '''
        This method returns the list of stopped download.
        offset: integer, the offset from the download waiting at the front.
        num: integer, the number of downloads to be returned.
        keys: keys for method response.
        return: The method response is of type list and its element is of type dict and it contains following keys.
        '''
        return self.server.aria2.tellStopped(offset, num, keys)

    def changePosition(self, gid, pos, how):
        '''
        This method changes the position of the download denoted by gid.
        gid: string, GID.
        pos: integer, the position relative which to be changed.
        how: string.
             POS_SET, it moves the download to a position relative to the beginning of the queue.
             POS_CUR, it moves the download to a position relative to the current position.
             POS_END, it moves the download to a position relative to the end of the queue.
        return: The response is of type integer and it is the destination position.
        '''
        return self.server.aria2.changePosition(gid, pos, how)

    def changeUri(self, gid, fileIndex, delUris, addUris, position=None):
        '''
        This method removes URIs in delUris from and appends URIs in addUris to download denoted by gid.
        gid: string, GID.
        fileIndex: integer, file to affect (1-based)
        delUris: list, URIs to be removed
        addUris: list, URIs to be added
        position: integer, where URIs are inserted, after URIs have been removed
        return: This method returns a list which contains 2 integers. The first integer is the number of URIs deleted. The second integer is the number of URIs added.
        '''
        return self.server.aria2.changeUri(gid, fileIndex, delUris, addUris, position)

    def getOption(self, gid):
        '''
        This method returns options of the download denoted by gid.
        gid: string, GID.
        return: The response is of type dict.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getOption', params))

    def changeOption(self, gid, options):
        '''
        This method changes options of the download denoted by gid dynamically.
        gid: string, GID.
        options: dict, the options.
        return: This method returns OK for success.
        '''
        params = [gid,options]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.changeOption', params))
        # return self.server.aria2.changeOption(gid, options)

    def getGlobalOption(self):
        '''
        This method returns global options.
        return: The method response is of type dict.
        '''
        return self.server.aria2.getGlobalOption()

    def changeGlobalOption(self, options):
        '''
        This method changes global options dynamically.
        options: dict, the options.
        return: This method returns OK for success.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.changeGlobalOption', options))


    def getGlobalStat(self):
        '''
        This method returns global statistics such as overall download and upload speed.
        return: The method response is of type struct and contains following keys.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getGlobalStat'))


    def purgeDownloadResult(self):
        '''
        This method purges completed/error/removed downloads to free memory.
        return: This method returns OK for success.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.purgeDownloadResult'))


    def removeDownloadResult(self, gid):
        '''
        This method removes completed/error/removed download denoted by gid from memory.
        return: This method returns OK for success.
        '''
        return self.server.aria2.removeDownloadResult(gid)

    def getVersion(self):
        '''
        This method returns version of the program and the list of enabled features.
        return: The method response is of type dict and contains following keys.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getSessionInfo'))


    def getSessionInfo(self):
        '''
        This method returns session information.
        return: The response is of type dict.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getSessionInfo'))


    def shutdown(self):
        '''
        This method shutdowns aria2.
        return: This method returns OK for success.
        '''
        return self.sendJsonRPC(self.server_uri, data=self.getRPCBody('aria2.shutdown'))


    def forceShutdown(self):
        '''
        This method shutdowns aria2.
        return: This method returns OK for success.
        '''
        return self.sendJsonRPC(self.server_uri, data=self.getRPCBody('aria2.forceShutdown'))


def isAria2Installed():
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and 'aria2c' in os.listdir(cmdpath):
            return True
    return False


def isAria2rpcRunning():
    pgrep_process = subprocess.Popen(
        'pgrep -l aria2', shell=True, stdout=subprocess.PIPE)
    if pgrep_process.stdout.readline() == b'':
        return False
    else:
        return True

if __name__=='__main__':
    ARIA2_HOST = "localhost"
    ARIA2_PORT = 6800
    ARIA2_SECRET = ""
    ARIA2_SCHEME = "http"


    try:
        p = PyAria2(host=ARIA2_HOST,
                    port=ARIA2_PORT,
                    secret=ARIA2_SECRET,
                    scheme=ARIA2_SCHEME)
        info=json.loads(p.getSessionInfo())[0]
        if info.get('error'):
            msg=info.get('error').get('message')
            if msg=='Unauthorized':
                msg='Aria2未验证！请检查Aria2信息！'
            print(msg)
        print(p)
    except Exception as e:
        print(e)
