from classes import DataGenerator


class ModelMapper:

    def __init__(self, application='current'):
        self.dg = DataGenerator()
        self.application = application
    

    """ 'Current' Object Definitions """

    def return_current_permission(self):
        return {
            "slug": self.dg.generate_string(32),
            "name": self.dg.generate_string(64),
            "description": self.dg.generate_string(128),
            "is_system": self.dg.generate_boolean()
        }

    def return_current_role(self):
        """ Returns a 'current' role object dictionary """
        return {
            "name": self.dg.generate_string(32),
            "description": self.dg.generate_string(128),
            "is_inheritable": self.dg.generate_boolean(),
            "permissions": []
        }

    def return_current_profile(self):
        """ Returns a 'current' profile object dictionary """
        return {
            "first_name": self.dg.generate_string(32),
            "roles": [],
            "permissions": []
        }


    """ Generic Methods """

    def return_n_objects(self, number_to_create, object_type):
        objects = []
        if self.application == 'current':
            for i in range(number_to_create):
                if object_type == 'permissions':
                    objects.append(self.return_current_permission())
                elif object_type == 'roles':
                    objects.append(self.return_current_role())
                elif object_type == 'profiles':
                    objects.append(self.return_current_profile())


        return objects
        
