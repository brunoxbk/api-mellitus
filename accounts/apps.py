from wagtail.users.apps import WagtailUsersAppConfig

class AccountsAppConfig(WagtailUsersAppConfig):
    user_viewset = "accounts.viewsets.UserViewSet"