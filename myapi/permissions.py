from rest_framework import permissions


# permission if can view / edit / create new board
class EditBoardOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        hasPermission = False
        if request.method in permissions.SAFE_METHODS:
            hasPermission = True

        # todo return true for post if has permission
        elif request.method == "PUT":
            hasPermission = request.user.has_perm("boards.can_edit_board")

        elif request.method == "POST":
            hasPermission = request.user.has_perm("boards.can_add_board")

        return hasPermission
