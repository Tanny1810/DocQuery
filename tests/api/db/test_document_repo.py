from unittest.mock import MagicMock

from api.app.db.repositories.document_repo import (
    create_document,
    update_document_status,
)
from api.app.constants.document_status import DocumentStatus


def test_create_document_uses_session_methods():
    """Ensure `create_document` constructs a Document and calls session methods
    without requiring a real database connection.
    """
    fake_db = MagicMock()

    doc = create_document(
        db=fake_db,
        original_filename="test.pdf",
        content_type="application/pdf",
        storage_provider="s3",
        storage_bucket="docquery-bucket",
        storage_key="documents/test.pdf",
        status_id=DocumentStatus.UPLOADED,
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
    fake_db = MagicMock()

    # Make query().filter(...).update(...) chainable
    query_mock = MagicMock()
    filter_mock = MagicMock()
    query_mock.filter.return_value = filter_mock
    filter_mock.update.return_value = 1
    fake_db.query.return_value = query_mock

    update_document_status(
        db=fake_db,
        document_id="some-id",
        status_id=DocumentStatus.PROCESSING,
    )

    fake_db.query.assert_called_once()
    query_mock.filter.assert_called_once()
    filter_mock.update.assert_called_once_with({"status_id": DocumentStatus.PROCESSING})
    fake_db.commit.assert_called_once()
