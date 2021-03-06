import pretend

from spaken import finder
from spaken.helpers import Requirement


def test_find():
    packages = [
        "django_healthchecks-1.4.0-py2.py3-none-any.whl",
        "django_healthchecks-1.3.0-py2.py3-none-any.whl",
        "django_healthchecks-1.3.1-py2.py3-none-any.whl",
    ]

    wheel_set = finder.WheelSet()
    for name in packages:
        wheel_set.add(name)

    whl = wheel_set.find(Requirement("django-healthchecks==1.4.0"))
    assert whl is not None
    assert whl.filename == "django_healthchecks-1.4.0-py2.py3-none-any.whl"

    whl = wheel_set.find(Requirement("django-healthchecks<1.4.0"))
    assert whl is not None
    assert whl.filename == "django_healthchecks-1.3.1-py2.py3-none-any.whl"

    whl = wheel_set.find(Requirement("django-healthchecks>=1.3.0,<1.4.0"))
    assert whl is not None
    assert whl.filename == "django_healthchecks-1.3.1-py2.py3-none-any.whl"

    whl = wheel_set.find(Requirement("django-healthchecks"))
    assert whl is not None
    assert whl.filename == "django_healthchecks-1.4.0-py2.py3-none-any.whl"


def test_invalid_file():
    packages = [
        "django_healthchecks-1.4.0-py2.py3-none-any.invalid",
    ]

    wheel_set = finder.WheelSet()
    for name in packages:
        wheel_set.add(name)

    whl = wheel_set.find(Requirement("django-healthchecks==1.4.0"))
    assert whl is None


def test_collect_filenames():
    filenames = [
        "django_healthchecks-1.4.0-py2.py3-none-any.invalid",
        "django_healthchecks-1.4.0-py2.py3-none-any.whl",
        "django_healthchecks-1.3.0-py2.py3-none-any.whl",
        "django-healthchecks-1.3.1-py2.py3-none-any.whl",
    ]

    requirements = [
        Requirement("Django-healthchecks==1.4.0"),
        Requirement("wsgi-basic-auth-healthchecks==1.1.0"),
    ]

    result, missing = finder.collect_filenames(filenames, requirements)
    assert result == ["django_healthchecks-1.4.0-py2.py3-none-any.whl"]
    assert missing == [Requirement("wsgi-basic-auth-healthchecks==1.1.0")]


def test_binary_package(monkeypatch):
    monkeypatch.setattr("sys.version_info", pretend.stub(major=3, minor=8))
    filenames = [
        "Pillow-7.0.0-cp37-cp37m-manylinux1_x86_64.whl",
    ]

    requirements = [
        Requirement("Pillow==7.0.0"),
    ]

    result, missing = finder.collect_filenames(filenames, requirements)
    assert result == []
