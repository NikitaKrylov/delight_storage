from django.contrib.auth.mixins import AccessMixin


class CheckUserConformity(AccessMixin):
    """set after LoginRequiredMixin and before view class"""
    permission_denied_message = "Пользователь несоответствует требуемому"

    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.get_user():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_user(self):
        """must be overriding"""
        return None
