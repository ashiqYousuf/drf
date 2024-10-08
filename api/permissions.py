from rest_framework import permissions


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # NOTE:- Not required (IsAdminUser does all the jazz)
    # def has_permission(self, request, view):
    #     if not request.user.is_staff:
    #         return False
    #     # user.get_all_permissions()
    #     # user.has_perm('products.view_product') # change | delete | add
    #     return super().has_permission(request, view)
