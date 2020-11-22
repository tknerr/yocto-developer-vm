import os

def test_picocom_package_is_installed_(host):
    assert host.package('picocom').is_installed

def test_picocom_command_is_found_(host):
    assert host.run('which picocom').rc is 0

def test_picocom_help_command_reports_version_info_(host):
    assert 'picocom v' in host.run('picocom --help').stdout

def test_dialout_group_exists_(host):
    assert host.group('dialout').exists

def test_user_is_in_dialout_group_(host):
    assert 'dialout' in host.user(f"{os.environ['USER']}").groups
