from yippee import group, pip

pip("click", "~=7.0")

with group("development"):
    pip("twine", "~=1.12.0")
    pip("black", "18.9b0")
    pip("flake8", "~=3.6.0")
    pip("wheel")

# run pipecleaner to generate three files:
#   requirements.txt
#   production-requirements.txt
#   development-requirements.txt
#
# these would be fully pinned denormalizations of all requirement
