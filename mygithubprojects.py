# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
from github import Github


class MyGithubProjects(object):
    """
    Get your projects and upstream projects you contribute to in Github.
    """

    def __init__(self, access_token, username):
        """
        Initialize MyGithubProjects instance.

        Args:
            access_token: Oauth access token for accessing your
                Github account.
            username: Your Github username.
        """
        self.github = Github(access_token)
        self.username = username
        self.cache = {}

    def reset(self):
        """
        Reset the cache for this instance.
        """
        self.cache = {}

    def get_projects(self):
        """
        Get a set of your project repos and upstream project repos you
        contribute to. This method caches the data fetched for future access.

        Returns:
            A tuple, (own_projects, upstream_projects) where
            own_projects and upstream_projects are sets of
            github.Repository.Repository instances
        """
        if self.cache.get('projects'):
            return (
                self.cache['projects']['own'],
                self.cache['projects']['upstream']
            )
        own_projects = set()
        upstream_projects = set()
        for repo in self.github.get_user().get_repos():
            if repo.fork:
                parent = repo.parent
                if parent in upstream_projects:
                    continue
                # Do not stop at any exception
                try:
                    if self.username in [
                            user.login for user in parent.get_contributors()]:
                        upstream_projects.add(repo.parent)
                except:
                    continue
            else:
                own_projects.add(repo)
        self.cache['projects'] = {
            'own': own_projects,
            'upstream': upstream_projects
        }
        if 'projects_dict' in self.cache:
            del self.cache['projects_dict']
        return (own_projects, upstream_projects)

    def get_project_details_dict(self, repo):
        """
        Get the details about a project from a project repo.

        Args:
            repo: A github.Repository.Repository instance

        Returns:
            A dictionary containing project details, e.g.,
            {
                'name': 'foo'
                'description': 'bar',
                'url': 'https://github.com/username/foo'
            }
        """
        name = repo.name
        description = repo.description
        url = repo.html_url
        return {
            'name': name,
            'description': description,
            'url': url
        }

    def get_projects_dict(self):
        """
        Get a dictionary containing data for your or upstream projects.
        This method also caches results for future use.

        Returns:
            A dictionary containing project data, e.g.,
            {
                'own': [
                    {
                        'name': 'foo'
                        'description': 'bar',
                        'url': 'https://github.com/username/foo'
                    }
                ],
                'upstream': [
                    {
                        'name': 'foo1'
                        'description': 'bar',
                        'url': 'https://github.com/username/foo1'
                    }
                ]
            }
        """
        if self.cache.get('projects_dict'):
            data = self.cache['projects_dict']
        else:
            data = {
                'upstream': [],
                'own': []
            }
            for repo in self.upstream_projects_iterator():
                data['upstream'].append(self.get_project_details_dict(repo))
            for repo in self.own_projects_iterator():
                data['own'].append(self.get_project_details_dict(repo))
        return data

    def get_projects_json(self):
        """
        Get a JSON output for your projects data.

        Returns:
            A JSON string.
        """
        data = self.get_projects_dict()
        return json.dumps(data, indent=2)

    def upstream_projects_iterator(self):
        """
        Get an iterator for all upstream project repos.
        """
        return iter(self.get_projects()[1])

    def own_projects_iterator(self):
        """
        Get an iterator for all own project repos.
        """
        return iter(self.get_projects()[0])

    def all_projects_iterator(self):
        """
        Get an iterator for all(own and upstream) project repos.
        """
        own, upstream = self.get_projects()
        return iter(own.union(upstream))
