import pulumi_github as github
from pulumi import ComponentResource, ResourceOptions

from iac.github.config import GitHubConfig


class GitHub(ComponentResource):
    def __init__(
        self,
        app_id: str,
        app_installation_id: str,
        app_private_key: str,
        config: GitHubConfig,
    ):
        super().__init__("aschbacd-labs:github", "github")

        # Provider and resource options
        provider = github.Provider(
            "aschbacd-labs",
            app_auth=github.ProviderAppAuthArgs(
                id=app_id,
                installation_id=app_installation_id,
                pem_file=app_private_key,
            ),
            owner="aschbacd-labs",
        )
        opts = ResourceOptions(parent=self, provider=provider)

        # Organization settings
        github.OrganizationSettings(
            "aschbacd-labs",
            name="aschbacd-labs",
            billing_email="testlab@dominikaschbacher.com",
            default_repository_permission="none",
            description="My personal test lab.",
            has_organization_projects=False,
            has_repository_projects=False,
            location="Austria",
            members_can_create_repositories=False,
            members_can_create_internal_repositories=False,
            members_can_create_private_repositories=False,
            members_can_create_public_repositories=False,
            members_can_create_pages=False,
            members_can_create_private_pages=False,
            members_can_create_public_pages=False,
            opts=opts.merge(ResourceOptions(protect=True)),
        )

        # Teams
        teams = {
            team.name: github.Team(
                team.name,
                name=team.name,
                description=team.description,
                opts=opts,
            )
            for team in config.teams
        }

        # Team members
        for team in config.teams:
            github.TeamMembers(
                team.name,
                team_id=teams[team.name].id,
                members=[
                    github.TeamMembersMemberArgs(username=member, role="member")
                    for member in team.members
                ],
                opts=opts,
            )

        # Repositories
        for repo in config.repositories:
            # Repository
            repository = github.Repository(
                repo.name,
                name=repo.name,
                description=repo.description,
                visibility=repo.visibility,
                has_issues=False,
                has_projects=False,
                has_wiki=False,
                auto_init=True,
                archive_on_destroy=True,
                allow_squash_merge=False,
                allow_rebase_merge=False,
                allow_auto_merge=False,
                allow_merge_commit=True,
                delete_branch_on_merge=True,
                opts=opts.merge(ResourceOptions(protect=True)),
            )

            # Topics
            if len(repo.topics) > 0:
                github.RepositoryTopics(
                    repo.name,
                    repository=repository.name,
                    topics=repo.topics,
                    opts=opts,
                )

            # Repository teams
            for team in repo.teams:
                github.TeamRepository(
                    f"{repo.name}-{team.name}",
                    team_id=teams[team.name].id,
                    repository=repository.name,
                    permission=team.permission,
                    opts=opts,
                )

            # Actions
            github.ActionsRepositoryPermissions(
                repo.name,
                repository=repository.name,
                enabled=repo.actions.enabled,
                allowed_actions="all",
                opts=opts,
            )

            for var in repo.actions.variables:
                github.ActionsVariable(
                    f"{repo.name}-{var.name}",
                    repository=repository.name,
                    variable_name=var.name,
                    value=var.value,
                    opts=opts,
                )

            for secret in repo.actions.secrets:
                github.ActionsSecret(
                    f"{repo.name}-{secret.name}",
                    repository=repository.name,
                    secret_name=secret.name,
                    plaintext_value=secret.value,
                    opts=opts,
                )
