# Storage Utilities

This repository provides Python utility wrappers for easy and unified access to major storage platforms:

- **MEGA.nz** (`mega_storage.py`)
- **Cloudflare R2** (`r2_storage.py`)
- **Supabase Storage** (`supabase_storage.py`)

Each utility offers user-friendly methods for common file operations such as uploads, downloads, listing files, generating public links, and more. This guide explains how to get started with each backend.

---

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/legeRise/storage-utilities.git
   cd storage-utilities
   ```

2. **Install dependencies:**
   All backends require Python 3.6+.

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is missing, install packages directly:
   ```
   pip install python-dotenv mega.py boto3 botocore supabase
   ```

3. **Set up environment variables**  
   Create a `.env` file at the root and fill in your credentials.  
   Refer to each section below for the required variables.

---

## 1. MEGA.nz Utility (`mega_storage.py`)

### Environment variables:

```
MEGA_STORAGE_EMAIL=your-mega-email
MEGA_STORAGE_PASSWORD=your-mega-password
```

### Basic usage:

```python
from mega_storage import MegaStorage

mega = MegaStorage()
# Upload a file
url = mega.upload_file("localfile.txt")
print("Upload URL:", url)

# List files
print(mega.list_files())

# Download a file
mega.download_file("file_on_mega.txt", dest_path="./downloads")
```

### Available methods:
- `upload_file(file_path, dest_folder=None)`
- `download_file(file_name, dest_path=".")`
- `get_link(name)`
- `delete(name)`
- `list_files()`
- `create_folder(folder_path)`
- `rename(old_name, new_name)`
- `import_from_url(url, dest_folder=None)`
- `get_storage(unit="MB")`

---

## 2. Cloudflare R2 Utility (`r2_storage.py`)

### Environment variables:

```
R2_BUCKET_NAME=your-bucket-name
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
```

### Basic usage:

```python
from r2_storage import R2Storage

r2 = R2Storage()
# Upload a file
url = r2.upload_file('backup.zip', 'localpath/backup.zip')
print("View URL:", url)

# List all files
print(r2.list_files())

# Generate a presigned upload URL for direct upload
upload_url = r2.generate_upload_url('myfile.txt')
print(upload_url)
```

### Available methods:
- `list_files(prefix="")`
- `list_files_with_times(prefix="")`
- `delete(key)`
- `get_view_url(key, expires_in=3600)`
- `clear_bucket()`
- `generate_upload_url(key, content_type, expires_in)`
- `upload_file(key, file_path, content_type)`
- `exists(key)`

---

## 3. Supabase Storage Utility (`supabase_storage.py`)

### Environment variables:

Add your Supabase credentials (often managed via Django `settings.py`, but `.env` works if importing directly):

```
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-service-key
```

### Basic usage:

```python
from supabase_storage import (
    list_files_in_folder,
    upload_file_to_bucket,
    delete_file_from_bucket,
    get_public_url,
)

bucket = "your-bucket"
folder = "your-folder"

# List files
print(list_files_in_folder(bucket, folder))

# Upload a file
upload_file_to_bucket("local.txt", bucket, folder, "remote.txt")

# Get a public URL
url = get_public_url(bucket, folder, "remote.txt")
print(url)
```

### Available methods:
- `list_files_in_folder(bucket_name, folder_name)`
- `upload_file_to_bucket(file_path, bucket_name, folder_name, file_name)`
- `delete_file_from_bucket(bucket_name, folder_name, file_name)`
- `get_public_url(bucket_name, folder_name, file_name)`

---

## Contributions

Feel free to submit pull requests for bug fixes or new storage integrations.

---

## License

MIT

---

**Questions?**  
Open an issue on [GitHub](https://github.com/legeRise/storage-utilities/issues), or reach out to the maintainer.
