from django.contrib.auth import get_user_model

from functional_tests.base import FunctionalTest
from django.conf import settings

from functional_tests.container_commands import create_session_on_server
from functional_tests.management.commands.create_session import create_pre_authenticated_session


User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email: str):
        if self.test_server:
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = '[email protected]'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
