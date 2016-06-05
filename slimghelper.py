import requests, json, base64, time, threading


class slimgHelper(object):
    """docstring for slimgHelper"""

    def __init__(self, client_id='', client_secret=''):
        super(slimgHelper, self).__init__()
        #Initializing properties

        # ID and Secret are found on the account page
        self.client_id = client_id
        self.client_secret = client_secret

        #To be filled in by getAccessRefreshTokens
        self.access_token = ''
        self.refresh_token = ''

        #Unused?
        self.expires_in = 85800

        #Default payload for 'anon' logins
        self.payload = {'client_id': client_id}

        #Header for 'anon' logins
        if (client_secret == ''):
            self.headers = {'Authorization': 'Client-ID '+client_id}
        else:
            self.headers = {}

    #Used in getting the dict from the JSON data
    def JsonAsDict(self, requestInstance):
        return json.loads(requestInstance.text)['data']

    #Used when using the Client ID and Access Token
    def getAccessRefreshTokens(self, returnTokens=False):
        url = 'https://api.sli.mg/token'
        payload = {'grant_type': 'client_credentials', 'client_id': self.client_id, 'client_secret': self.client_secret}
        response = requests.post(url, data=payload)
        json_dict = json.loads(response.text)
        print json_dict
        self.access_token = json_dict['access_token']
        self.refresh_token = json_dict['refresh_token']

        # Subtracting 10 mins from expires_in lowers the risk of the user trying to do something with a bad token.
        # Still unused.
        self.expires_in = (json_dict['expires_in'] - 600)
        self.payload = {'client_id': self.client_id, 'access_token': self.access_token}

        if (returnTokens):
            return {'access_token': self.access_token, 'refresh_token': self.refresh_token}
        else:
            return True

    def getUserAlbums(self, username):
        url = 'https://api.sli.mg/account/{}/albums/'.format(username)
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))

    def getUserMedia(self, username, page=1):
        url = 'https://api.sli.mg/account/{}/media/{}'.format(username, page)
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))['media']

    # ---Endpoint section seperation--- #

    def getMediaInfo(self, mediaKey):
        url = 'https://api.sli.mg/media/{}'.format(mediaKey)
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))

    def waitingForUpload(self, mediaKey):
        currentInfo = self.getMediaInfo(mediaKey)
        currentStatus = currentInfo['status']
        if (currentStatus == 20 or currentStatus == 21):
            time.sleep(3)
            return self.waitingForUpload(mediaKey)
        else:
            return currentInfo

    def createMedia(self, type, data, size=None, title=None, description=None, shared=None, albumKey=None,
                    albumSecret=None, tags=None, waitForUploadCompletionForDataReturn=False):
        url = 'https://api.sli.mg/media'

        if (type == 'binary'):
            with open(data, 'rb') as f:
                dataName = data
                type = 'base64'
                data = 'data:image/{}'.format(dataName.split('.')[-1]) + ';base64,' + base64.b64encode(f.read())

        payload = {}

        payload.update(self.payload)

        payload.update({'type': type, 'data': data})

        payload.update({'size': size,
                        'title': title,
                        'description': description,
                        'shared': shared,
                        'album_key': albumKey,
                        'album_secret': albumSecret,
                        'tags': tags
                        })

        # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-values-from-a-dict
        payload = dict((k, v) for k, v in payload.iteritems() if v)

        json_data = self.JsonAsDict(requests.post(url, data=self.payload, headers=self.headers))
        if (waitForUploadCompletionForDataReturn == False):
            return json_data
        elif (waitForUploadCompletionForDataReturn):
            return self.waitingForUpload(json_data['media_key'])

    def updateMedia(self, mediaKey, title=None, description=None, shared=None, albumKey=None,
                    albumSecret='', tags=None, mediaSecret=''):

        url = 'https://api.sli.mg/media/{}/{}'.format(mediaKey, mediaSecret)

        payload = {}

        payload.update(self.payload)

        payload.update({'title': title,
                        'description': description,
                        'shared': shared,
                        'album_key': albumKey,
                        'album_secret': albumSecret,
                        'tags': tags
                        })

        # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-values-from-a-dict
        payload = dict((k, v) for k, v in payload.iteritems() if v)

        return self.JsonAsDict(requests.post(url, data=self.payload, headers=self.headers))

    def deleteMedia(self, mediaKey, mediaSecret = ''):
        url = 'https://api.sli.mg/media/{}/{}'.format(mediaKey, mediaSecret)

        return self.JsonAsDict(requests.delete(url, params=self.payload, headers=self.headers))

    # ---Endpoint section seperation--- #

    def getAlbumInfo(self, albumKey):
        url = 'https://api.sli.mg/album/{}'.format(albumKey)
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))

    def createAlbum(self, description=None, shared=None, mediaKeys=None, mediaSecrets=None, tags=None):
        url = 'https://api.sli.mg/album'

        payload = {}

        payload.update(self.payload)

        if(mediaKeys is not None):
            mediaKeys = ','.join(mediaKeys)

        if(mediaSecrets is not None):
            mediaSecrets = ','.join(mediaSecrets)

        payload.update({'description': description,
                        'shared': shared,
                        'media_keys': mediaKeys,
                        'media_secrets': mediaSecrets,
                        'tags': tags
                        })

        # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-values-from-a-dict
        payload = dict((k, v) for k, v in payload.iteritems() if v)

        return self.JsonAsDict(requests.post(url, data=self.payload, headers=self.headers))

    def updateAlbum(self, albumKey, description=None, shared=None, mediaKeys=None, mediaSecrets=None, tags=None, albumSecret=''):
        url = 'https://api.sli.mg/album/{}/{}'.format(albumKey, albumSecret)

        payload = {}

        payload.update(self.payload)

        if (mediaKeys is not None):
            mediaKeys = ','.join(mediaKeys)

        if (mediaSecrets is not None):
            mediaSecrets = ','.join(mediaSecrets)

        payload.update({'description': description,
                        'shared': shared,
                        'media_keys': mediaKeys,
                        'media_secrets': mediaSecrets,
                        'tags': tags
                        })

        # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-values-from-a-dict
        payload = dict((k, v) for k, v in payload.iteritems() if v)
        print payload
        print url

        return self.JsonAsDict(requests.post(url, data=payload, headers=self.headers))

    def deleteAlbum(self, albumKey, albumSecret=''):
        url = 'https://api.sli.mg/album/{}/{}'.format(albumKey, albumSecret)

        return self.JsonAsDict(requests.delete(url, params=self.payload, headers=self.headers))

    def getAlbumMedia(self, albumKey):
        url = 'https://api.sli.mg/album/{}/media'.format(albumKey)
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))['media']

    # ---Endpoint section seperation--- #

    def browsePublic(self, page=1):
        url = 'https://api.sli.mg/browse/{}'.format(page)
        print url
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))

    def browsePublicByTag(self, tag, type='sfw', page=1):
        url = 'https://api.sli.mg/browse/{}/{}/{}'.format(tag, type, page)
        return self.JsonAsDict(requests.get(url, params=self.payload, headers=self.headers))