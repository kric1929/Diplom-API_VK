import time
import json
import requests

ACCESS_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class User:

    def __init__(self, token):
        self.token = token
        self.id = 171691064
        self.friends_groups_list = []
        self.result_list = []
        self.list_id = []

    def get_params(self):
        return {
            'access_token': ACCESS_TOKEN,
            'v': 5.103
        }

    def get_friends(self):
        params = self.get_params()
        params['user_id'] = self.id
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()

    def get_groups(self):
        params = self.get_params()
        params['user_id'] = self.id
        params['extended'] = 1
        params['fields'] = 'members_count'
        response = requests.get('https://api.vk.com/method/groups.get', params)
        return response.json()['response']['items']

    def get_groups_friends(self):
        for friends in self.get_friends()['response']['items']:
            params = self.get_params()
            params['user_id'] = friends
            time.sleep(0.3)
            friends_groups = requests.get('https://api.vk.com/method/groups.get', params)
            if 'response' in friends_groups.json():
                self.friends_groups_list.extend(friends_groups.json()['response']['items'])
                print('.')
        return self.friends_groups_list

    def matches_in_groups(self):
        for groups_id in self.get_groups():
            self.list_id.append(groups_id['id'])
            groups = list(set(self.list_id) - set(self.friends_groups_list))
            if groups_id['id'] in groups:
                self.result_list.append({
                    "name": groups_id['name'],
                    "gid": groups_id['id'],
                    "members_count": groups_id['members_count']
                })

    def write_in_json_file(self):
        with open('groups.json', 'w') as f:
            json.dump(self.result_list, f, ensure_ascii=False)


if __name__ == '__main__':
    user = User(ACCESS_TOKEN)
    user.get_groups_friends()
    user.matches_in_groups()
    user.write_in_json_file()
    print('Выполнено!')
