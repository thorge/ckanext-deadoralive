"""The deadoralive plugin."""

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.deadoralive.model.results as results
import ckanext.deadoralive.config as config
import ckanext.deadoralive.logic.action.get as get
import ckanext.deadoralive.logic.action.update as update
import ckanext.deadoralive.helpers as helpers
import ckanext.deadoralive.logic.auth.update
import ckanext.deadoralive.logic.auth.get
from ckanext.deadoralive.views import default
from flask import Blueprint


class DeadOrAlivePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions)

    # Blueprint

    def get_blueprint(self):
        blueprint = Blueprint('deadoralive', self.__module__)
        blueprint.add_url_rule(
            '/deadoralive/get_resources_to_check', view_func=default.get_resources_to_check)
        blueprint.add_url_rule(
            '/deadoralive/get_url_for_resource_id', view_func=default.get_resource_id_for_url)
        blueprint.add_url_rule(
            '/deadoralive/upsert', view_func=default.upsert, methods=['POST'])
        blueprint.add_url_rule(
            '/deadoralive/organization/broken_links/', view_func=default.broken_links_by_organization)
        blueprint.add_url_rule(
            '/ckan-admin/broken_links', view_func=default.broken_links_by_email)
        return [blueprint]

    # IConfigurable

    def configure(self, config_):
        results.create_database_table()

        # Update the class variables for the config settings with the values
        # from the config file, *if* they're in the config file.
        config.recheck_resources_after = toolkit.asint(config_.get(
            "ckanext.deadoralive.recheck_resources_after",
            config.recheck_resources_after))
        config.resend_pending_resources_after = toolkit.asint(
            config_.get(
                "ckanext.deadoralive.resend_pending_resources_after",
                config.resend_pending_resources_after))
        config.broken_resource_min_fails = toolkit.asint(
            config_.get(
                "ckanext.deadoralive.broken_resource_min_fails",
                config.broken_resource_min_fails))
        config.broken_resource_min_hours = toolkit.asint(
            config_.get(
                "ckanext.deadoralive.broken_resource_min_hours",
                config.broken_resource_min_hours))
        config.authorized_users = toolkit.aslist(
            config_.get(
                "ckanext.deadoralive.authorized_users",
                config.authorized_users))

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('assets', 'deadoralive')

        if toolkit.check_ckan_version(max_version='2.2.999'):
            # Add CKAN version 2.2 support templates.
            toolkit.add_template_directory(config_, '2.2_templates')

    # IActions

    def get_actions(self):
        return {
            "ckanext_deadoralive_get_resources_to_check":
                get.get_resources_to_check,
            "ckanext_deadoralive_upsert": update.upsert,
            "ckanext_deadoralive_get": get.get,
            "ckanext_deadoralive_broken_links_by_organization":
                get.broken_links_by_organization,
            "ckanext_deadoralive_broken_links_by_email":
                get.broken_links_by_email,
        }

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "ckanext_deadoralive_get": helpers.get_results,
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            "ckanext_deadoralive_upsert":
                ckanext.deadoralive.logic.auth.update.upsert,
            "ckanext_deadoralive_get_resources_to_check":
                ckanext.deadoralive.logic.auth.get.get_resources_to_check,
            "ckanext_deadoralive_get":
                ckanext.deadoralive.logic.auth.get.get,
            "ckanext_deadoralive_broken_links_by_organization":
                ckanext.deadoralive.logic.auth.get.broken_links_by_organization,
            "ckanext_deadoralive_broken_links_by_email":
                ckanext.deadoralive.logic.auth.get.broken_links_by_email,
        }
