from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        'ver_servico': True,
        'edit_service': True,
        'delete_service': True,
        'add_service': True,
        'view_user': True,
        'edit_user': True,
        'delete_user': True,
        'add_user': True,
    }
class LongisticUser(AbstractUserRole):
    available_permissions = {
        'ver_servico': True,
        'edit_service': True,
        'delete_service': False,
        'add_service': False,
        'view_user': False,
        'edit_user': False,
        'delete_user': False,
        'add_user': False,
    }
class User(AbstractUserRole):
    available_permissions = {
        'ver_servico': True,
        'edit_service': False,
        'delete_service': False,
        'add_service': False,
        'view_user': True,
        'edit_user': False,
        'delete_user': False,
        'add_user': False,
    }