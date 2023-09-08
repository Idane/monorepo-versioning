import git
import os
import semver
import sys

repo = git.Repo(".")

libRoot = os.path.join(os.getcwd(), "lib")

def get_current_lib_version(libName):
    tags = list(filter(lambda tag: tag.name.startswith(libName), repo.tags))
    if not tags:
        latest = "0.0.0"
    else:
        by_version = sorted(tags, key=lambda tag: tag.commit.committed_datetime)
        tagName = by_version[-1].name
        _, latest = tagName.rsplit("-", 1)

    return semver.Version.parse(latest)
def bump_version(version):
    ## todo: semantic commit based bumping
    return version.bump_patch()

if __name__ == "__main__":
    projects = sys.argv[1:]
    for project in projects:
        current_version = get_current_lib_version(project)
        bumped = bump_version(current_version)
        repo.create_tag(f"{project}-{bumped}")