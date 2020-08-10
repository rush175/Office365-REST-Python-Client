from unittest import TestCase

from settings import settings

from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.providers.acs_token_provider import ACSTokenProvider
from office365.runtime.auth.providers.saml_token_provider import SamlTokenProvider
from office365.runtime.auth.token_response import TokenResponse
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext


user_credentials = UserCredential(settings.get('user_credentials').get('username'),
                                  settings.get('user_credentials').get('password'))


class TestSharePointClient(TestCase):

    def test1_connect_with_app_principal(self):
        credentials = ClientCredential(settings.get('client_credentials').get('client_id'),
                                       settings.get('client_credentials').get('client_secret'))
        ctx = ClientContext.connect_with_credentials(settings['url'], credentials)
        self.assertIsInstance(ctx.authentication_context.provider, ACSTokenProvider)
        self.assertIsInstance(ctx.authentication_context.provider.token, TokenResponse)
        self.assertTrue(ctx.authentication_context.provider.token.is_valid)

    def test2_connect_with_user_credentials(self):
        ctx = ClientContext.connect_with_credentials(settings['url'], user_credentials)
        self.assertIsInstance(ctx.authentication_context.provider, SamlTokenProvider)

    def test3_init_from_url(self):
        ctx = ClientContext.from_url(settings['url']).with_credentials(user_credentials)
        web = ctx.web.load().execute_query()
        self.assertIsNotNone(web.url)

    def test4_connect_with_client_cert(self):
        pass

    def test5_get_batch_request(self):
        client = ClientContext(settings['url']).with_credentials(user_credentials)
        current_user = client.web.currentUser
        client.load(current_user)
        current_web = client.web
        client.load(current_web)
        client.execute_batch()
        self.assertIsNotNone(current_web.url)
        self.assertIsNotNone(current_user.user_id)

    def test6_update_batch_request(self):
        pass
        #client = ClientContext(settings['url']).with_credentials(user_credentials)
        #list_item = client.web.get_file_by_server_relative_url("/SitePages/Home.aspx").listItemAllFields
        #new_title = "Page %s" % random_seed
        #list_item.set_property("Title", new_title)
        #list_item.update()
        #client.execute_batch()
        #self.assertIsNotNone(list_item)