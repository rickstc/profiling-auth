import requests
import classes
import random

def check_permissions(profiles, permissions, num_checks):
    current_api = classes.APIInterface('current')
    successful_checks = 0

    for i in range(num_checks):
        profile = random.choice(profiles)
        permission = random.choice(permissions)
        existed = current_api.check_permission(profile, permission['slug'])
        if existed:
            successful_checks = successful_checks + 1

    return successful_checks

    

def select_relations_for_object(children, owner, num_relations, type):
    for i in range(num_relations):
        c = random.choice(children)
        owner[type].append(c['id'])
        permissions = list(filter(lambda i: i['id'] != c['id'], children))
    return owner

def setup_relations(children, owners, owner_type, num_relations, children_type):
    """ Takes a list of permissions and grants n permissions to the object """
    current_api = classes.APIInterface('current')
    for o in owners:
        o = select_relations_for_object(children, o, num_relations, children_type)
        current_api.update_object(owner_type, o)
    return owners

def setup_current(num_permissions, num_roles, num_profiles):
    """ Sets up default objects """
    current_api = classes.APIInterface('current')
    permissions = create_current_objects(num_permissions, 'permissions')
    roles = create_current_objects(num_roles, 'roles')
    profiles = create_current_objects(num_profiles, 'profiles')
    return permissions, roles, profiles


def cleanup():
    """ Cleans up DB in between test runs """
    current_api = classes.APIInterface('current')
    current_api.delete_objects('permissions')
    current_api.delete_objects('roles')
    current_api.delete_objects('profiles')

def create_current_objects(number_to_create, type):
    """ Creates Current Permissions """
    current_api = classes.APIInterface('current')
    mapper = classes.ModelMapper('current')
    for p in mapper.return_n_objects(number_to_create, type):
        current_api.create_object(type, p)
    return current_api.get_objects(type)

def init():


    num_permissions = 10
    num_roles = 10
    num_profiles = 10

    permissions_per_role = 2
    roles_per_profile = 2
    permissions_per_profile = 2

    num_permission_checks = 10


    timer = classes.RequestTimer()

    cleanup()

    timer.start_timer()
    
    print("Setting up users")

    # Generate the objects used in the tests
    permissions, roles, profiles = setup_current(num_permissions, num_roles, num_profiles)
    print(f'It took {timer.get_elapsed_time()} seconds to set up objects')
    
    timer.restart_timer()

    # Add permissions to roles
    roles = setup_relations(permissions, roles, 'roles', permissions_per_role, 'permissions')
    print(f'It took {timer.get_elapsed_time()} seconds to add {permissions_per_role} permissions to each role')

    timer.restart_timer()

    # Add roles to profiles
    setup_relations(roles, profiles, 'profiles', roles_per_profile, 'roles')
    print(f'It took {timer.get_elapsed_time()} seconds to add {roles_per_profile} roles to each profile')

    timer.restart_timer()

    # Add permissions to profiles
    setup_relations(permissions, profiles, 'profiles', permissions_per_profile, 'permissions')
    print(f'It took {timer.get_elapsed_time()} seconds to add {permissions_per_profile} permissions to each profile')

    timer.restart_timer()


    # Check Permissions
    successful_checks = check_permissions(profiles, permissions, num_permission_checks)

    print(f'It took {timer.get_elapsed_time()} seconds to check {num_permission_checks} permissions')
    print(f'The profile had the permission {successful_checks} out of {num_permission_checks} times.')


    timer.end_timer()

    print(f"Total Time: {timer.get_final_time()}")




if __name__ == '__main__':
    init()