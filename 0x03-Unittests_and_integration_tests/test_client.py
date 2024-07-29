#!/usr/bin/env python3
"""test client module"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient, PropertyMock
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json', return_value={'some_key': 'some_value'})
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        client = GithubOrgClient(org_name)
        result = client.org
        URL = "https://api.github.com/orgs/{org_name}"
        URL1 = "https://api.github.com/orgs/google/repos"

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(f"URL")

        # Assert the returned value is as expected (based on mock return_value)
        self.assertEqual(result, {'some_key': 'some_value'})

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property."""
        # Mocked payload for org property
        mocked_payload = {'repos_url': 'URL1'}
        mock_org.return_value = mocked_payload

        # Initialize the client with a test org name
        client = GithubOrgClient('google')

        # Access _public_repos_url and check if it returns the expected URL
        result = client._public_repos_url
        self.assertEqual(result, mocked_payload['repos_url'])

    @patch('client.get_json',
           return_value=[{'name': 'repo1'}, {'name': 'repo2'}])
    @patch.object(GithubOrgClient, '_public_repos_url',
                  new_callable=PropertyMock, return_value='URL1')
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test the public_repos method."""
        client = GithubOrgClient('google')

        # Call the method and capture the output
        result = client.public_repos

        # Expected result based on the mocked payload
        expected_repos = ['repo1', 'repo2']
        self.assertEqual(result, expected_repos)

        # Assert that _public_repos_url and get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with('URL1')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": {"key": "my_license"}}, "other_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test the has_license method."""
        client = GithubOrgClient('test_org')
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test suite for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up the class-wide fixtures and mock requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Mock responses based on URL
        def side_effect(url):
            if url == f"https://api.github.com/orgs/{org_payload['login']}":
                return Mock(json=lambda: org_payload)
            elif url == org_payload['repos_url']:
                return Mock(json=lambda: repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration setup."""
        client = GithubOrgClient(org_payload['login'])
        repos = client.public_repos
        self.assertEqual(repos, self.expected_repos)

    def test_has_license(self):
        """Test has_license method for filtering repos with 'apache-2.0' license."""
        client = GithubOrgClient(org_payload['login'])
        repos = client.public_repos
        apache2_repos = [repo for repo in repos if client.has_license(repo, 'apache-2.0')]
        self.assertEqual(apache2_repos, self.apache2_repos)

    @parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test suite for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up the class-wide fixtures and mock requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Mock responses based on URL
        def side_effect(url):
            if url == f"https://api.github.com/orgs/{org_payload['login']}":
                return Mock(json=lambda: org_payload)
            elif url == org_payload['repos_url']:
                return Mock(json=lambda: repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration setup."""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method filtering by 'apache-2.0' license."""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
