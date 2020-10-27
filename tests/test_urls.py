import pytest
import yaml

from no_more_qs import NoMoreQS


def load_yaml(path):
    with open(path, "r") as stream:
        yml = yaml.safe_load(stream)

    return yml

urls = load_yaml("tests/test_case/urls.yml")


@pytest.fixture(scope="function", params=urls)
def url(request):
    return request.param

def test_urls_in_strict_mode(url):
    nmq = NoMoreQS()
    assert nmq.clean(url["input"]) == url["output"]

def test_exclude_fld():
    url = {
        "input": "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia&fbclid=IwAR2NasdasdasdadasdfP58isTW-c3U",
        "output": "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia"
    }

    nmq = NoMoreQS(exclude_flds=('youtube.com'))
    assert nmq.clean(url["input"]) == url["output"]


def test_include_fld():
    url = {
        "input": "https://www.youtube.com/watch?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia&fbclid=IwAR2NasdasdasdadasdfP58isTW-c3U",
        "output": "https://www.youtube.com/watch?v=h-RHH79hzHI"
    }

    nmq = NoMoreQS(include_flds=('youtube.com'))
    assert nmq.clean(url["input"]) == url["output"]


def test_remove_fbclid():
    nmq = NoMoreQS(strict=False)
    url = urls[2]
    assert NoMoreQS.remove_fbclid(url["input"]) == url["output"]
    assert nmq.clean(url["input"]) == url["output"]
