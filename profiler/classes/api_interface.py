import requests

class APIInterface:
    def __init__(self, url_path):
        self.url_path = url_path


    def send_request(self, url, method, expected_status, data=None):
        if method is 'get':
            response = requests.get(url)
        elif method is 'put':
            response = requests.put(url, data)
        elif method is 'delete':
            response = requests.delete(url)
            if response.status_code == expected_status:
                return True
        else:
            response = requests.post(url, data)


        if response.status_code == 400:
            print(f'Bad Request at {url}')
            print(response.json())
            print(data)

        if expected_status == 'any':
            if response.status_code == 200:
                return True
            return False

        if response.status_code != expected_status:
            print(f'Something went wrong with the {method} request to: {url}')
            print(response.status_code)
            print(response.json())
            print(data)
            return False

        return response.json()




    """ Get Object """

    def get_objects(self, type):
        """ Gets all objects of type """
        url = f'http://localhost/{self.url_path}/{type}/'
        return self.send_request(url, 'get', 200)

    def delete_objects(self, type):
        """ Deletes all objects of type """
        objects = self.get_objects(type)
        if objects == False:
            return True
        if len(objects) == 0:
            return True

        for o in objects:
            url = f'http://localhost/{self.url_path}/{type}/{o["id"]}/'
            self.send_request(url, 'delete', 204)

        objects = self.get_objects(type)
        if objects == False:
            return True
        return len(objects)

    def create_object(self, type, object_dict):
        """ Creates an object of a given type """
        url = f'http://localhost/{self.url_path}/{type}/'
        return self.send_request(url, 'post', 201, object_dict)

    def update_object(self, type, object_dict):
        url = f'http://localhost/{self.url_path}/{type}/{object_dict["id"]}/'
        return self.send_request(url, 'put', 200, object_dict)

    def check_permission(self, profile, permission_slug):
        url = f'http://localhost/{self.url_path}/profiles/{profile["id"]}/check/'
        return self.send_request(url, 'post', 'any', {"permission_slug": permission_slug})