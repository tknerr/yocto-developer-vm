import pytest

def test_vscode_apt_sources_list_exists_(host):
    assert host.file('/etc/apt/sources.list.d/packages_microsoft_com_repos_vscode.list').exists

def test_vscode_apt_key_defined_(host):
    assert 'Microsoft (Release signing) <gpgsecurity@microsoft.com>' in host.run('apt-key list').stdout

def test_vscode_package_is_installed_(host):
    assert host.package('code').is_installed

def test_vscode_command_is_found_(host):
    assert host.run('which code').rc is 0
