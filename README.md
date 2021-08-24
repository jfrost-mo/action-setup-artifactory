# action-setup-artifactory
Github action to configure connection to Artifactory for a workflow job.

The action writes the following files to the Github runner to enable
communication with Artifactory for Python:

* ~/.netrc
* ~/.config/pip/pip.conf


Usage
-----

```yaml
- uses: MetOffice/action-setup-artifactory@v1
  with:
    # Artifactory username. This is usually a user/team email address
    # Default: ${{ secrets.ART_USER}}
    username: ''

    # Artifactory API key. This can be obtained by logging into Artifactory
    # with either username/password or SSO.
    # Default: ${{ secrets.ART_KEY}}
    api-key: ''
```
