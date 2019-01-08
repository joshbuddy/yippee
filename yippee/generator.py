import venv
import os
import subprocess
from functools import reduce


class Generator:
    def __init__(self, config):
        self.config = config
        self.state = config.state
        self.excluded = config.state["exclude"]
        self.group_dependencies = {}
        self.groups = {}
        for name in self.state["groups"].keys():
            cls = (
                TopLevelGroupGenerator if name == "_top_level_group" else GroupGenerator
            )
            self.groups[name] = cls(name, self.state["groups"][name], self.excluded)

    def generate(self):
        self.preflight()
        self.install()
        self.write_requirements()

    def preflight(self):
        for group in self.groups.values():
            group.generate_environments()
            group.install_existing_requirements()
            group.write_temp_requirements()

    def install(self):
        for group in self.groups.values():
            group.install_freeze_requirements()

    def write_requirements(self):
        common_dependencies = reduce(
            lambda x, y: x & y,
            (map(lambda d: set(d.dependencies), self.groups.values())),
        )

        for group in self.groups.values():
            group.write_requirements(common_dependencies)


class GroupGenerator:
    def __init__(self, name, packages, excluded):
        self.name = name
        self.packages = packages
        self.excluded = excluded
        self.env_dir = ".env-%s" % name
        self.temp_requirements_path = ".temp-requirements-%s.txt" % name
        self.requirements_path = "requirements-%s.txt" % name

    @property
    def pip_path(self):
        return os.path.join(self.env_dir, "bin", "pip")

    def generate_environments(self):
        if not os.path.isdir(self.env_dir):
            builder = venv.EnvBuilder(with_pip=True)
            builder.create(self.env_dir)

    def install_existing_requirements(self):
        if os.path.isfile(self.requirements_path):
            subprocess.check_call(
                [self.pip_path, "install", "-r", self.requirements_path]
            )

    def write_temp_requirements(self):
        with open(self.temp_requirements_path, "w") as fh:
            fh.write("-r ")
            fh.write(TopLevelGroupGenerator.temp_requirements_path)
            fh.write("\n")

            for package in self.packages:
                req_line = "".join(package)
                fh.write(req_line)
                fh.write("\n")

    def install_freeze_requirements(self):
        subprocess.check_call(
            [self.pip_path, "install", "-r", self.temp_requirements_path]
        )
        out = subprocess.check_output([self.pip_path, "freeze", "--all"])
        with open(self.temp_requirements_path, "wb") as fh:
            fh.write(out)

        lines = out.decode().strip().split("\n")

        self.dependencies = lines
        print(lines)

    def write_requirements(self, common_dependencies):
        requirements = self.process_requirements(common_dependencies)
        package_names = set(map(lambda p: p[0], self.packages))
        excluded_packages = list(
            filter(lambda e: e not in package_names, self.excluded)
        )

        with open(self.requirements_path, "w") as fh:
            for dep in requirements:
                if dep.split("==")[0] in excluded_packages:
                    continue
                fh.write(dep)
                fh.write("\n")

        os.remove(self.temp_requirements_path)

    def process_requirements(self, common_dependencies):
        requirements = ["-r " + TopLevelGroupGenerator.requirements_path]
        with open(self.temp_requirements_path, "r") as in_fh:
            for line in in_fh:
                if line.strip() not in common_dependencies:
                    requirements.append(line.strip())
        return requirements


class TopLevelGroupGenerator(GroupGenerator):
    env_dir = ".env"
    temp_requirements_path = ".temp-requirements.txt"
    requirements_path = "requirements.txt"

    def __init__(self, name, packages, excluded):
        self.name = name
        self.packages = packages
        self.excluded = excluded

    def process_requirements(self, common_dependencies):
        sorted_deps = list(common_dependencies)
        sorted_deps.sort()
        return sorted_deps

    def write_temp_requirements(self):
        with open(self.temp_requirements_path, "w") as fh:
            for package in self.packages:
                req_line = "".join(package)
                fh.write(req_line)
                fh.write("\n")
