from rest_framework.permissions import BasePermission

from jetty import settings
from jetty.utils.backend import project_auth


class HasProjectPermissions(BasePermission):
    token_prefix = 'Token '

    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token or token[:len(self.token_prefix)] != self.token_prefix:
            return False

        token = token[len(self.token_prefix):]

        return project_auth(token)


class ModifyNotInDemo(BasePermission):

    def has_permission(self, request, view):
        if not settings.JETTY_DEMO:
            return True
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return False
        return True
