#!/usr/bin/env python3
"""test client module"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient, PropertyMock


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


if __name__ == '__main__':
    unittest.main()
