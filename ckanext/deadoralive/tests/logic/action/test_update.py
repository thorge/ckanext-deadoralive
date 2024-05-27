# -*- coding: utf-8 -*-
"""Tests for logic/action/update.py."""

import ckan.new_tests.helpers as helpers

import ckanext.deadoralive.tests.helpers as custom_helpers
import ckanext.deadoralive.tests.factories as factories


class TestUpsert(custom_helpers.FunctionalTestBaseClass):

    def test_upsert(self):
        """Simple test: call upsert() then call get() and check the result."""
        resource = factories.Resource()

        helpers.call_action("ckanext_deadoralive_upsert",
                            resource_id=resource["id"], alive=True,
                            status=200, reason="OK")

        result = helpers.call_action("ckanext_deadoralive_get",
                                     resource_id=resource["id"])

        assert result["resource_id"] == resource["id"]
        assert result["alive"] is True
        assert result["status"] == 200
        assert result["reason"] == "OK"

    def test_upsert_with_unicode(self):
        """Test unicode strings with non-ASCII chars in the result."""
        resource = factories.Resource()

        helpers.call_action("ckanext_deadoralive_upsert",
                            resource_id=resource["id"], alive=True,
                            status=200, reason="Alleß ökäy!")

        result = helpers.call_action("ckanext_deadoralive_get",
                                     resource_id=resource["id"])

        assert result["resource_id"] == resource["id"]
        assert result["alive"] is True
        assert result["status"] == 200
        assert result["reason"] == "Alleß ökäy!"
