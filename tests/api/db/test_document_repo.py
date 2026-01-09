import importlib.util
import os
from unittest.mock import MagicMock


def _load_repo_module():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    path = os.path.join(base, "api", "app", "db", "repositories", "document_repo.py")
    spec = importlib.util.spec_from_file_location("document_repo", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_constants_module():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    path = os.path.join(base, "api", "app", "constants", "document_status.py")
    spec = importlib.util.spec_from_file_location("document_status", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_create_document_uses_session_methods():
    repo = _load_repo_module()
    fake_db = MagicMock()

    doc = repo.create_document(
        db=fake_db,
        original_filename="test.pdf",
        content_type="application/pdf",
        storage_provider="s3",
        storage_bucket="docquery-bucket",
        storage_key="documents/test.pdf",
        status_id=1,
    )

    # The returned object should have the attributes set from input
    assert doc.original_filename == "test.pdf"
    assert doc.content_type == "application/pdf"
    assert doc.storage_provider == "s3"
    assert doc.storage_bucket == "docquery-bucket"
    assert doc.storage_key == "documents/test.pdf"
    assert doc.status_id == 1

    # and the repository should call session.add, commit and refresh
    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()


def test_update_document_status_calls_update_and_commit():
    repo = _load_repo_module()
    consts = _load_constants_module()

    fake_db = MagicMock()

    # Make query().filter(...).update(...) chainable
    query_mock = MagicMock()
    filter_mock = MagicMock()
    query_mock.filter.return_value = filter_mock
    filter_mock.update.return_value = 1
    fake_db.query.return_value = query_mock

    repo.update_document_status(
        db=fake_db,
        document_id="some-id",
        status_id=consts.DocumentStatus.PROCESSING,
    )

    fake_db.query.assert_called_once()
    query_mock.filter.assert_called_once()
    filter_mock.update.assert_called_once_with(
        {"status_id": consts.DocumentStatus.PROCESSING}
    )
    fake_db.commit.assert_called_once()
