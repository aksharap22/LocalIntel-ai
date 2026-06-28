# API Documentation

## `GET /health`

Returns offline and model status.

## `POST /upload`

Multipart form upload with field `file`.

## `POST /process?id={id}`

Processes a previously uploaded file.

## `GET /documents`

Returns processed records.

## `GET /document/{id}`

Returns one processed record.

## `GET /search`

Query parameters:

- `keyword`
- `entity`
- `title`
- `category`
- `date`

## `GET /analytics`

Returns totals, latest uploads, type counts, priority counts, and average processing time.

## `GET /export/json`

Downloads all processed records as JSON.

## `GET /export/csv`

Downloads all processed records as CSV.

## `DELETE /document/{id}`

Deletes one file and associated processed data.
