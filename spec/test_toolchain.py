import pytest

@pytest.mark.parametrize('pkg', [
    'bc',
    'build-essential',
    'chrpath',
    'cpio',
    'diffstat',
    'gawk',
    'git',
    'python3',
    'python3-distutils',
    'texinfo',
    'wget',
    'vim'
])
def test_prerequisite_packages_are_installed_(host, pkg):
    assert host.package(pkg).is_installed

