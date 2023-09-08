import git
import os
import semver
import sys

repo = git.Repo(".")

def get_current_project_version(projectName):
    print(f"Getting version for {f}")
    tags = list(filter(lambda tag: tag.name.startswith(projectName), repo.tags))
    if not tags:
        latest = "0.0.0"
    else:
        by_version = sorted(tags, key=lambda tag: tag.commit.committed_datetime)
        tagName = by_version[-1].name
        _, latest = tagName.rsplit("-", 1)
    print(f"Current version for {projectName} is {latest}")
    return semver.Version.parse(latest)
def bump_version(version):
    bumped = version.bump_patch()
    print(f"Bumping {version} to {bumped}")
    ## todo: semantic commit based bumping
    return bumped

if __name__ == "__main__":
    projects = sys.argv[1:]
    for project in projects:
        current_version = get_current_project_version(project)
        bumped = bump_version(current_version)
        repo.create_tag(f"{project}-{bumped}")