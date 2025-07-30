import pytest

from building_blocks.abstractions.result import Err, Ok, Result, ResultAccessError


class FakeOk(Ok[str, None]):
    def __init__(self, value: str) -> None:
        self._value = value


class FakeErr(Err[None, str]):
    def __init__(self, error: str) -> None:
        self._error = error


class TestResult:
    def test_value_when_is_ok_then_return_value(self) -> None:
        result: Ok[str, str] = Ok("success")

        expected_value = "success"
        assert result.value == expected_value

        with pytest.raises(ResultAccessError):
            _ = Err("failure").value

    def test_err_is_err(self) -> None:
        result: Err[str, str] = Err("failure")

        expected_error = "failure"
        assert result.error == expected_error

        with pytest.raises(ResultAccessError):
            _ = Ok("success").error

    def test_ok_repr(self) -> None:
        result: Ok[int, int] = Ok(42)

        assert repr(result) == "Ok(42)"

    def test_err_repr(self) -> None:
        result: Err[str, str] = Err("bad things")

        assert repr(result) == "Err('bad things')"

    def test_inheritance(self) -> None:
        res: Result[int, str] = Ok(5)

        assert isinstance(res, Result) is True
        assert isinstance(res, Ok)

        res2: Result[int, str] = Err("fail")

        assert isinstance(res2, Result)
        assert isinstance(res2, Err)
