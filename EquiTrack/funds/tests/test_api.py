# Python imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rest_framework import status
from tablib.core import Dataset
from unittest import TestCase

from EquiTrack.factories import (
    FundsReservationHeaderFactory,
    FundsReservationItemFactory,
    UserFactory,
)
from EquiTrack.tests.mixins import APITenantTestCase, URLAssertionMixin


class UrlsTestCase(URLAssertionMixin, TestCase):
    '''Simple test case to verify URL reversal'''
    def test_urls(self):
        '''Verify URL pattern names generate the URLs we expect them to.'''
        names_and_paths = (
            ('frs', 'frs/', {}),
            ('funds-reservation-header', 'reservation-header/', {}),
            ('funds-reservation-item', 'reservation-item/', {}),
        )
        self.assertReversal(names_and_paths, 'funds:', '/api/v2/funds/')


class TestFundsReservationHeaderExportList(APITenantTestCase):
    def setUp(self):
        super(TestFundsReservationHeaderExportList, self).setUp()
        self.unicef_staff = UserFactory(is_staff=True)
        self.frs = FundsReservationHeaderFactory()

    def test_invalid_format_export_api(self):
        response = self.forced_auth_req(
            'get',
            '/api/v2/funds/reservation-header/',
            user=self.unicef_staff,
            data={"format": "unknown"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_csv_export_api(self):
        response = self.forced_auth_req(
            'get',
            '/api/v2/funds/reservation-header/',
            user=self.unicef_staff,
            data={"format": "csv"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dataset = Dataset().load(response.content, 'csv')
        self.assertEqual(dataset.height, 1)
        self.assertEqual(dataset._get_headers(), [
            "Reference Number",
            "Vendor Code",
            "Number",
            "Document Date",
            "Type",
            "Currency",
            "Document Text",
            "Amount",
            "Total Amount",
            "Actual Amount",
            "Outstanding Amount",
            "Start Date",
            "End Date",
        ])
        self.assertEqual(dataset[0], (
            u"{}".format(self.frs.intervention.pk),
            u"{}".format(self.frs.vendor_code),
            unicode(self.frs.fr_number),
            u"{}".format(self.frs.document_date),
            u"{}".format(self.frs.fr_type),
            u"{}".format(self.frs.currency),
            u"{}".format(self.frs.document_text),
            u"{}".format(self.frs.intervention_amt),
            u"{}".format(self.frs.total_amt),
            u"{}".format(self.frs.actual_amt),
            u"{}".format(self.frs.outstanding_amt),
            u"{}".format(self.frs.start_date),
            u"{}".format(self.frs.end_date),
        ))

    def test_csv_flat_export_api(self):
        response = self.forced_auth_req(
            'get',
            '/api/v2/funds/reservation-header/',
            user=self.unicef_staff,
            data={"format": "csv_flat"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dataset = Dataset().load(response.content, 'csv')
        self.assertEqual(dataset.height, 1)
        self.assertEqual(dataset._get_headers(), [
            "Id",
            "Reference Number",
            "Vendor Code",
            "Number",
            "Document Date",
            "Type",
            "Currency",
            "Document Text",
            "Amount",
            "Total Amount",
            "Actual Amount",
            "Outstanding Amount",
            "Start Date",
            "End Date",
        ])
        self.assertEqual(dataset[0], (
            u"{}".format(self.frs.pk),
            u"{}".format(self.frs.intervention.number),
            u"{}".format(self.frs.vendor_code),
            unicode(self.frs.fr_number),
            u"{}".format(self.frs.document_date),
            u"{}".format(self.frs.fr_type),
            u"{}".format(self.frs.currency),
            u"{}".format(self.frs.document_text),
            u"{}".format(self.frs.intervention_amt),
            u"{}".format(self.frs.total_amt),
            u"{}".format(self.frs.actual_amt),
            u"{}".format(self.frs.outstanding_amt),
            u"{}".format(self.frs.start_date),
            u"{}".format(self.frs.end_date),
        ))


class TestFundsReservationItemExportList(APITenantTestCase):
    def setUp(self):
        super(TestFundsReservationItemExportList, self).setUp()
        self.unicef_staff = UserFactory(is_staff=True)
        self.frs = FundsReservationHeaderFactory()
        self.item = FundsReservationItemFactory(
            fund_reservation=self.frs
        )

    def test_invalid_format_export_api(self):
        response = self.forced_auth_req(
            'get',
            '/api/v2/funds/reservation-item/',
            user=self.unicef_staff,
            data={"format": "unknown"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_csv_export_api(self):
        response = self.forced_auth_req(
            'get',
            '/api/v2/funds/reservation-item/',
            user=self.unicef_staff,
            data={"format": "csv"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dataset = Dataset().load(response.content, 'csv')
        self.assertEqual(dataset.height, 1)
        self.assertEqual(dataset._get_headers(), [
            "Reference Number",
            "Fund Reservation Number",
            "Item Number",
            "Line Item",
            "Description",
            "WBS",
            "Grant Number",
            "Fund",
            "Overall Amount",
            "Overall Amount DC",
            "Due Date",
        ])
        self.assertEqual(dataset[0], (
            u"{}".format(self.frs.intervention.pk),
            unicode(self.frs.pk),
            u"{}".format(self.item.fr_ref_number),
            u"{}".format(self.item.line_item),
            u"",
            u"",
            u"",
            u"",
            u"{0:.2f}".format(self.item.overall_amount),
            u"{0:.2f}".format(self.item.overall_amount_dc),
            u"",
        ))

    def test_csv_flat_export_api(self):
        response = self.forced_auth_req(
            'get',
            '/api/v2/funds/reservation-item/',
            user=self.unicef_staff,
            data={"format": "csv_flat"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dataset = Dataset().load(response.content, 'csv')
        self.assertEqual(dataset.height, 1)
        self.assertEqual(dataset._get_headers(), [
            "Id",
            "Reference Number",
            "Fund Reservation Number",
            "Item Number",
            "Line Item",
            "Description",
            "WBS",
            "Grant Number",
            "Fund",
            "Overall Amount",
            "Overall Amount DC",
            "Due Date",
        ])
        self.assertEqual(dataset[0], (
            u"{}".format(self.item.pk),
            u"{}".format(self.frs.intervention.number),
            unicode(self.frs.fr_number),
            u"{}".format(self.item.fr_ref_number),
            u"{}".format(self.item.line_item),
            u"",
            u"",
            u"",
            u"",
            u"{0:.2f}".format(self.item.overall_amount),
            u"{0:.2f}".format(self.item.overall_amount_dc),
            u"",
        ))
