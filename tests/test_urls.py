import pytest
import yaml
from no_more_qs import NoMoreQS, qs_delta


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


pure_url = "https://github.com/EltonChou/no-more-query-string"
fuzzy_allowed_qs = "?v=h-RHH79hzHI&feature=emb_logo&ab_channel=Ceia"
fbclid = "&fbclid=IwAR2NasdasdasdadasdfP58isTW-c3U"


def test_exclude_fld():
    url = {
        "input": f"{pure_url}{fuzzy_allowed_qs}{fbclid}",
        "output": f"{pure_url}{fuzzy_allowed_qs}"
    }

    nmq = NoMoreQS(exclude_flds=('github.com'))
    assert nmq.clean(url["input"]) == url["output"]


def test_include_fld():
    url = {
        "input": f"{pure_url}{fuzzy_allowed_qs}{fbclid}",
        "output":  f"{pure_url}"
    }

    nmq = NoMoreQS(include_flds=('github.com'))
    assert nmq.clean(url["input"]) == url["output"]


def test_remove_fbclid():
    nmq = NoMoreQS(strict=False)
    url = urls[2]
    assert NoMoreQS.remove_fbclid(url["input"]) == url["output"]
    assert nmq.clean(url["input"]) == url["output"]


def test_qs_complement(url):
    complement = qs_delta(url["input"], url["output"])
    assert sorted(url["complement"]) == sorted(list(complement))
