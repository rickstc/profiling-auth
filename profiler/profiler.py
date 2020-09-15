import requests
import classes
import random

def check_permissions(application_name, profiles, permissions, num_checks):
    api = classes.APIInterface(application_name)
    successful_checks = 0
    
    for i in range(num_checks):
        profile = random.choice(profiles)
        permission = random.choice(permissions)
        if type(permission) is str:
            existed = api.check_permission(profile, permission)
        else:
            existed = api.check_permission(profile, permission['slug'])
        if existed:
            successful_checks = successful_checks + 1

    return successful_checks

def assign_relations(owner, children, child_type, num_relations):
    temp = children.copy()
    for i in range(num_relations):
        c = random.choice(temp)
        if type(c) == dict:
            owner[child_type].append(c['id'])
            temp = list(filter(lambda i: i['id'] != c['id'], temp))
        else:
            owner[child_type].append(c)
            temp.remove(c)
    return owner

def setup_relations(application_name, owners, owner_type, children, child_type, num_relations):
    """ This flexible function accepts an owner (role or profile), and children (permissions or roles), and assigns the correct number of relations """
    api = classes.APIInterface(application_name)
    for owner in owners:
        owner = assign_relations(owner, children, child_type, num_relations)
        api.update_object(owner_type, owner)
    return api.get_objects(owner_type)

def setup_data(application_name, num_permissions, num_roles, num_profiles):
    """ Returns permissions, roles, profiles to be used in the application """
    permissions = create_objects(application_name, num_permissions, 'permissions')
    roles = create_objects(application_name, num_roles, 'roles')
    profiles = create_objects(application_name, num_profiles, 'profiles')
    return permissions, roles, profiles



def create_objects(application_name, number_to_create, object_type):
    """ Creates objects in the API """
    mapper = classes.ModelMapper(application_name)
    api = classes.APIInterface(application_name)
    if application_name == 'proposed' and object_type == 'permissions':
        return mapper.return_n_objects(number_to_create, object_type)

    for ob in mapper.return_n_objects(number_to_create, object_type):
        api.create_object(object_type, ob)
    return api.get_objects(object_type)

def cleanup(app):
    """ Cleans up DB in between test runs """
    if app == 'current':
        current_api = classes.APIInterface('current')
        current_api.delete_objects('permissions')
        current_api.delete_objects('roles')
        current_api.delete_objects('profiles')
    else:
        proposed_api = classes.APIInterface('proposed')
        proposed_api.delete_objects('roles')
        proposed_api.delete_objects('profiles')


def profile_application(
        application_name,
        num_permissions,
        num_roles,
        num_profiles,
        permissions_per_role,
        roles_per_profile,
        permissions_per_profile,
        num_permission_checks
    ):

    #cleanup(application_name)
    print(f"*********** PROFILING {str.upper(application_name)} ***********")
    
    timer = classes.RequestTimer()
    timer.start_timer()

    # Generate the objects used in the tests
    permissions, roles, profiles = setup_data(application_name, num_permissions, num_roles, num_profiles)
    print(f'It took {timer.get_elapsed_time()} seconds to set up objects')
    timer.restart_timer()

    # Add permissions to roles
    roles = setup_relations(application_name, roles, 'roles', permissions, 'permissions', permissions_per_role)
    print(f'It took {timer.get_elapsed_time()} seconds to add {permissions_per_role} permissions to each role')
    timer.restart_timer()

    # Add roles to profiles
    profiles = setup_relations(application_name, profiles, 'profiles', roles, 'roles', roles_per_profile)
    print(f'It took {timer.get_elapsed_time()} seconds to add {roles_per_profile} roles to each profile')
    timer.restart_timer()

    # Add permissions to profiles
    profiles = setup_relations(application_name, profiles, 'profiles', permissions, 'permissions', permissions_per_profile)
    print(f'It took {timer.get_elapsed_time()} seconds to add {permissions_per_profile} permissions to each profile')
    timer.restart_timer()


    # Check Permissions
    successful_checks = check_permissions(application_name, profiles, permissions, num_permission_checks)

    print(f'It took {timer.get_elapsed_time()} seconds to check {num_permission_checks} permissions')
    print(f'The profile had the permission {successful_checks} out of {num_permission_checks} times.')


    timer.end_timer()

    print(f"Total Time: {timer.get_final_time()}")


def init():

    num_permissions = 50
    num_roles = 17
    num_profiles = 10000

    permissions_per_role = 35
    roles_per_profile = 2
    permissions_per_profile = 2

    num_permission_checks = 10000

    profile_application('current', num_permissions, num_roles, num_profiles, permissions_per_role, roles_per_profile, permissions_per_profile, num_permission_checks)
    profile_application('proposed', num_permissions, num_roles, num_profiles, permissions_per_role, roles_per_profile, permissions_per_profile, num_permission_checks)
    

if __name__ == '__main__':
    init()