from rest_framework import permissions

class MyUserPermissions(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are

     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """
    def has_object_permission(self, request, view, obj):
       #import pdb; pdb.set_trace()
       #return obj.from_user == request.user
       return obj.id == request.user.id
      # return obj is None or obj.from_user == request.user
