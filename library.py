import requests
from gi.repository import Notify

base_url = 'https://api.twitch.tv/kraken/'
client_id = 'pvv7ytxj4v7i10h0p3s7ewf4vpoz5fc'
head = {'Accept': 'application/vnd.twitch.v2+json',
        'Client-ID': client_id}


class NotifyApi(object):
    '''
    Represents all twitch and libnotify/gobject calls the program needs
    '''
    nick = ''
    verbose = False

    def __init__(self, nick, verbose=False):
        '''
        Initialize the object with a nick and verbose option

        Positional arguments:
        nick - nickname of the user
        verbose - if we should be verbose in output
        '''
        if not nick.strip():
            raise ValueError('nick passed to __init__ is empty')
        if (
                not isinstance(nick, str) or
                not isinstance(verbose, bool)
                ):
            raise TypeError('Invalid variable type passed to NotifyApi')

        self.nick = nick
        self.verbose = verbose

        if not Notify.init('TwitchNotifier'):
            raise RuntimeError('Failed to init libnotify')

    def get_followed_channels(self, payload={}):
        '''
        Get a list of channels the user is following

        Positional arguments:
        payload - dictionary converted to args passed in a GET request

        Raises:
        NameError - when the current nickname is invalid

        Returns a list of channels that user follows
        '''
        url = base_url + '/users/' + self.nick + '/follows/channels'

        try:
            r = requests.get(url, headers=head, params=payload)
        except Exception as e:
            print('[ERROR] Exception in get_followed_channels::requests.get()',
                  '\n[ERROR] __doc__ = ' + str(e.__doc__))
            return []

        try:
            json = r.json()
        except ValueError:
            print('[ERROR] Failed to parse json in get_followed_channels. '
                  'A empty json object was created')
            json = {}
            if self.verbose:
                print('r.text: ' + r.text, '\nr. status_code: ' +
                      str(r.status_code), '\nr.headers: ' + str(r.headers))

        if ('status' in json and json['status'] == 404):
            raise NameError(self.nick + ' is a invalid nickname!')

        ret = []
        if 'follows' in json:
            for chan in json['follows']:
                ret.append(chan['channel']['name'])

        return ret

    def __del__(self):
        '''Uninit libnotify object'''
        Notify.uninit()

    def check_if_online(chan, verb=False):
        '''
        Gets a stream object and sees if it's online

        Positional arguments:
        chan - channel name

        Returns True/False if channel is off/of, None if error occurs
        '''
        url = base_url + '/streams/' + chan

        try:
            r = requests.get(url, headers=head)
        except Exception as e:
            print('[ERROR] Exception in check_if_online::requests.get()',
                  '\n[ERROR] __doc__ = ' + str(e.__doc__))
            return None

        try:
            json = r.json()
        except ValueError:
            print('[ERROR] Failed to parse json in check_if_online. ')
            if verb:
                print('r.text: ' + r.text, '\nr. status_code: ' +
                      str(r.status_code), '\nr.headers: ' + str(r.headers))
            return None

        if ('stream' in json and json['stream'] is None) or 'error' in json:
            return False
        else:
            return True

    def show_notification(self, title, message):
        '''
        Show a notification using libnotify/gobject

        Positional arguments:
        title - notification title
        message - notification message

        Raises:
        RuntimeError - failed to show the notification
        '''
        n = Notify.Notification.new(title, message, 'dialog-information')

        if not n.show():
            raise RuntimeError('Failed to show a notification')

    def get_status(self):
        '''
        Get a list of lists in format of [name, True/False/None]
        True = channel is online, False = channel is offline, None = error
        '''
        ret = []
        offset = 0
        limit = 100

        while True:
            fol = self.get_followed_channels({'offset': offset,
                                              'limit': limit})
            for chan in fol:
                ret.append([chan, None])

            if len(fol) == 0:
                break

            offset = offset + limit

        url = base_url + 'streams?channel=' + ','.join(elem[0] for elem in ret)

        try:
            r = requests.get(url, headers=head)
        except Exception as e:
            print('[ERROR] Exception in get_status::requests.get()',
                  '\n[ERROR] __doc__ = ' + str(e.__doc__))
            return ret

        try:
            json = r.json()
        except ValueError:
            print('[ERROR] Failed to parse json in get_status. ')
            return ret

        for el in ret:
            if 'streams' in json:
                for stream in json['streams']:
                    if stream['channel']['name'] == el[0]:
                        el[1] = True

        # Turn all None channels into False
        # Because we have already passed the part with exceptions
        for el in ret:
            if el[1] is None:
                el[1] = False

        return ret

    def diff(self, new, old):
        '''
        Computes diff between two lists returned from get_status() and notifies

        Positional arguments:
        new - newer list returned from get_status()
        old - older list returned from get_status()
        '''
        i = 0
        while (i < len(new) - 1) and (i < len(old) - 1):
            if not new[i][1] is None and not old[i][1] is None:
                if new[i][0] == old[i][0] and new[i][1] and not old[i][1]:
                    try:
                        self.show_notification(new[i][0], "came online")
                    except RuntimeError:
                        print('[ERROR] Failed to show notification!\n'
                              '' + new[i][0] + ' came online')

                if new[i][0] == old[i][0] and not new[i][1] and old[i][1]:
                    try:
                        self.show_notification(new[i][0], "went offline")
                    except RuntimeError:
                        print('[ERROR] Failed to show notification!\n'
                              '' + new[i][0] + ' went offline')
            i = i + 1

if __name__ == '__main__':
    core = NotifyApi('Xangold')
    list_of_chans = core.get_followed_channels()
    print(list_of_chans, len(list_of_chans))
    stat = core.get_status()
    print(NotifyApi.check_if_online('nadeshot'))
    print(stat)
