# iac

Resource management via Pulumi

## Local development

**Dependencies:**

* [direnv](https://github.com/direnv/direnv)
* [python](https://github.com/pyenv/pyenv) (v3.12)
* [poetry](https://github.com/python-poetry/poetry)

**Setup:**

1. clone this repository & cd into it
1. run `direnv allow`
1. copy the Pulumi encryption passphrase from KeePass to `.passphrase`

## GitHub

The GitHub organization `aschbacd-labs` is managed by this repository. This repository uses GitHub
Actions to deploy changes to repositories or the organization.

### Teams and Permissions

Teams and their members are defined in `Pulumi.github.prod.yaml`.

### Repositories

Repositories are defined in `Pulumi.github.prod.yaml`.

### Branch protection

Branch protection is not supported because of GitHub free tier.
