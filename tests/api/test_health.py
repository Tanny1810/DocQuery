import ast
import os


def _read_source(path_parts):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(base, *path_parts)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_health_returns_healthy_literal():
    """Statically parse `health.py` to ensure the handler returns
    a `HealthResponse` with status set to the literal 'healthy'.
    """
    src = _read_source(("api", "app", "routers", "v1", "health.py"))
    tree = ast.parse(src)

    func = next(
        n
        for n in tree.body
        if (isinstance(n, ast.FunctionDef) or isinstance(n, ast.AsyncFunctionDef))
        and n.name == "health_check"
    )

    # find the return statement
    ret = next((n for n in ast.walk(func) if isinstance(n, ast.Return)), None)
    assert ret is not None

    # Expect a call like HealthResponse(status="healthy")
    call = ret.value
    assert isinstance(call, ast.Call)
    # check keywords for status value
    kw = {k.arg: k.value for k in call.keywords}
    assert "status" in kw
    assert isinstance(kw["status"], ast.Constant)
    assert kw["status"].value == "healthy"
