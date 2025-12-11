class Dataset:
    """Represents a dataset in the Data Science module."""

    def __init__(self, dataset_id: int, name: str, rows: int, columns: int, uploaded_by: str, upload_date: str):
        self.dataset_id = dataset_id
        self.name = name
        self.rows = rows
        self.columns = columns
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date

    def get_id(self):
        return self.dataset_id

    def get_name(self):
        return self.name

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def get_uploaded_by(self):
        return self.uploaded_by

    def get_upload_date(self):
        return self.upload_date

    def __str__(self):
        return f"Dataset {self.dataset_id}: {self.name} ({self.rows} rows, {self.columns} columns, uploaded_by={self.uploaded_by})"