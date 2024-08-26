#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyactionnetwork.models import Donation, Tag, Tagging


def get_all_resource(resource, cls, api, url, resources=[]):
    """Get a list of all resources for an organization.
    Args:
        resource (str):
            resource name (e.g. 'links', 'people', etc.)
        cls (class):
            A class from the models module representing the resource (Tag, Person, etc.)
        api (pyactionnetwork.ActionNetworkApi):
            Authorized ActionNetwork API instance.
        url (str):
            URL of the endpoint to use.
        resources (list):
            List of cls instances.

    Returns:
        (list) List of Donations processed by AN.
    """

    data = api.request_json("GET", url)
    resources += [cls(data=d) for d in data['_embedded'][f"osdi:{resource}"]]

    if data.get('_links', {}).get('next', None):
        next_url = data.get('_links').get('next').get('href')
        return get_all_resource(resource=resource, cls=cls, api=api, url=next_url, resources=resources)
    return resources

def get_all_donations(api=None, url=None):
    """Get a list of all donations for an organization.

    Args:
        api (pyactionnetwork.ActionNetworkApi):
            Authorized ActionNetwork API instance.
        url (str):
            URL of the donations endpoint to use. Defaults to all
            donations made to a group.

    Returns:
        (list) List of Donations processed by AN.
    """
    if not url:
        url = api.resource_to_url("donations")

    return get_all_resource("donations", Donation, api=api, url=url)

def get_all_tags(api=None, url=None):
    """Get a list of all tags for an organization.

    Args:
        api (pyactionnetwork.ActionNetworkApi):
            Authorized ActionNetwork API instance.
        url (str):
            URL of the tags endpoint to use. Defaults to all
            tags made to a group.

    Returns:
        (list) List of Tag on AN.
    """
    if not url:
        url = api.resource_to_url("tags")

    return get_all_resource("tags", Tag, api=api, url=url)

def get_all_taggings(api=None, url=None):
    """Get a list of all taggings for an organization.

    Args:
        api (pyactionnetwork.ActionNetworkApi):
            Authorized ActionNetwork API instance.
        url (str):
            URL of the taggings endpoint to use. Defaults to all
            taggings made to a group.

    Returns:
        (list) List of Tagging on AN.
    """
    if not url:
        url = api.resource_to_url("taggings")

    return get_all_resource("taggings", Tagging, api=api, url=url)
