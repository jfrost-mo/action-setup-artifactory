# Setup Artifactory Action
Github action to configure connection to Met Office Artifactory for a workflow job.

The action writes the following files to the Github runner to enable
communication with Artifactory for Python:

| File                       | Reason                                                       |
| -------------------------- | ------------------------------------------------------------ |
| ``~/.netrc``               | Add the provided Artifactory credentials                     |
| ``~/condarc``              | Add the ``channel_alias`` to point to Artifactory for conda. |
| ``~/.config/pip/pip.conf`` | Add the ``index-url`` to point to Artifactory for pip.       |


Usage
-----

```yaml
- uses: MetOffice/action-setup-artifactory@v1
  with:
    # Artifactory username. This is usually a user/team email address
    # Note: For Artifactory Access Tokens (no associated username) do not specify
    # this field or leave it blank.
    username: ''

    # Artifactory API key. This can be obtained by logging into Artifactory
    # with either username/password or SSO.
    api-key: ''

    # Authentication credentials check.
    # Confirms that username and api-key are active and working.
    # Default: false
    check-creds: true/false

    # Optional flag to use ``conda-forge`` as a conda channel in preference to the
    # Anaconda "defaults" channels. Enabling this option will also remove any
    # channels matching ``conda-main``, ``conda-r``, ``conda-free`` or ``defaults``
    # to avoid unintentional use of any Anaconda licensed channels. Also sets
    # strict channel priority.
    # Default: false
    setup-conda-forge: true/false
```

Examples
--------

Configure Artifactory using github secrets `ART_USER` and `ART_KEY` and
and check authentication credentials are active:

```yaml
jobs:
  my-job:
    steps:
        # Specifying username and api key
      - name: Set up Artifactory connection
        uses: MetOffice/action-setup-artifactory@v1
        with:
          username: ${{ secrets.USERNAME }}
          api-key: ${{ secrets.API_KEY }}
          check-creds: true

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.8"

      - name: Install Package from Artifactory
        run: pip install some-package-on-artifactory
```

Configure Artifactory using an **Access Token** (no associated username):
```yaml
jobs:
  my-job:
    steps:
        # Specify just Access Token
      - name: Set up Artifactory connection
        uses: MetOffice/action-setup-artifactory@v1
        with:
          api-key: ${{ secrets.ACCESS_TOKEN }}
          check-creds: true

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.8"

      - name: Install Package from Artifactory
        run: pip install some-package-on-artifactory
```
