from rest_framework import permissions


# permission if can view / edit / create new board
class EditBoardOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # todo return true for post if has permission
        return (request.user.has_perm("boards.can_edit_board") and request.method == "PUT")
