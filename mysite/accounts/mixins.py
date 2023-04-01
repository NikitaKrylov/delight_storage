from django.contrib.auth.mixins import AccessMixin

from posts.models import Post


class CheckUserConformity(AccessMixin):
    """set after LoginRequiredMixin and before view class"""
    permission_denied_message = "Пользователь несоответствует требуемому"
    raise_exception = True
    model = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user == self._get_user():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def _get_user(self):
        obj = self.get_object()
        if self.model is Post:
            return obj.author

        raise NotImplementedError("Type '{}' not implemented".format(type(obj)))
