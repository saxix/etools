
from django.utils import six

from etools.applications.EquiTrack.tests.cases import BaseTenantTestCase
from etools.applications.management.models import FlaggedIssue
from etools.applications.management.tests.factories import FlaggedIssueFactory
from etools.applications.partners.tests.factories import PartnerFactory


class TestStrUnicode(BaseTenantTestCase):
    '''Ensure calling six.text_type() on model instances returns the right text.'''

    def test_flagged_issue(self):
        partner = PartnerFactory()
        issue = FlaggedIssueFactory(
            content_object=partner,
            issue_id="321",
            message='test message'
        )
        self.assertEqual(six.text_type(issue), u"test message")

        issue = FlaggedIssueFactory(
            content_object=partner,
            issue_id="321",
            message=u"R\xe4dda Barnen"
        )
        self.assertEqual(six.text_type(issue), u"R\xe4dda Barnen")


class FlaggedIssueTest(BaseTenantTestCase):

    @classmethod
    def tearDownClass(cls):
        FlaggedIssue.objects.all().delete()
        super(FlaggedIssueTest, cls).tearDownClass()

    def test_get_or_new_creates_new_unsaved(self):
        partner = PartnerFactory()
        issue = FlaggedIssue.get_or_new(partner, 'test-new-unsaved')
        # make sure we got a new one
        self.assertTrue(issue.pk is None)

    def test_get_or_new_returns_saved(self):
        issue_id = 'test-return-saved'
        partner = PartnerFactory()
        issue = FlaggedIssueFactory(
            content_object=partner,
            issue_id=issue_id,
            message='test message'
        )
        self.assertTrue(issue.pk is not None)
        issue_back = FlaggedIssue.get_or_new(partner, issue_id)
        # make sure we got the same one back
        self.assertEqual(issue.pk, issue_back.pk)