import ast
import os


def _read_source(path_parts):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(base, *path_parts)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_config_defines_expected_classes_and_fields():
    """Statically analyze `api/app/core/config.py` to ensure expected
    configuration classes and fields exist without executing the module.
    """
    src = _read_source(("api", "app", "core", "config.py"))
    tree = ast.parse(src)

    class_names = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}

    # expected nested config classes
    expected_classes = {
        "CloudConfig",
        "QueueConfig",
        "DBConfig",
        "LLMConfig",
        "Settings",
    }
    assert expected_classes.issubset(class_names)

    # Inspect `Settings` class for presence of common attributes
    settings_node = next(
        n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Settings"
    )
    assigned = set()
    for node in settings_node.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assigned.add(node.target.id)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)

    for attr in (
        "APP_NAME",
        "ENV",
        "CLOUD_CONFIG",
        "QUEUE_CONFIG",
        "DB_CONFIG",
        "LLM_CONFIG",
    ):
        assert attr in assigned
