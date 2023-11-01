from abc import ABC, abstractmethod

from cruds.user_crud import create_user, get_user, update_user, delete_user


class Command(ABC):
    @abstractmethod
    def execute(self, request, url_parameter=None):
        pass


class CreateUserCommand(Command):
    def execute(self, request, url_parameter=None):
        return create_user(request)


class GetUserCommand(Command):
    def execute(self, request, url_parameter=None):
        return get_user(request, url_parameter)


class UpdateUserCommand(Command):
    def execute(self, request, url_parameter=None):
        return update_user(request)


class DeleteUserCommand(Command):
    def execute(self, request, url_parameter=None):
        return delete_user(request)
