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


def test_url_dequote():
    nmq = NoMoreQS()
    url = "http://techfeed.today/2016/06/21/" \
        "%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88%E5%B8%AB%E5%8D%B3%E5%B0%87%E5%A4%B1%E6%" \
        "A5%AD%EF%BC%9F%E4%BA%BA%E9%A1%9E%E5%B0%87%E5%83%8F%E9%A6%B4%E7%8B%97%E4%B8%80" \
        "%E6%A8%A3%E8%A8%93%E7%B7%B4%E9%9B%BB%E8%85%A6/"
    assert nmq.clean(url, dequote=True) == "http://techfeed.today/2016/06/21/程式設計師即將失業？人類將像馴狗一樣訓練電腦/"


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
