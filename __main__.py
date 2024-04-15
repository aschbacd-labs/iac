import pulumi

from iac.github.config import GitHubConfig
from iac.github.github import GitHub

config = pulumi.Config()

# GitHub config
if config.get("github"):
    gh_app_id = config.require("gh-app-id")
    gh_app_installation_id = config.require("gh-app-installation-id")
    gh_app_private_key = config.require("gh-app-private-key")
    gh_config: GitHubConfig = GitHubConfig.model_validate(config.require_object("github"))

    GitHub(
        app_id=gh_app_id,
        app_installation_id=gh_app_installation_id,
        app_private_key=gh_app_private_key,
        config=gh_config,
    )
