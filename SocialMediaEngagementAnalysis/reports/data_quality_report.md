# Data Quality Report

This report is based on the local sample dataset used for demonstration and validation.

## Before-and-after summary
- Original rows: 30
- Rows after cleaning: 30
- Duplicate rows removed: 0
- Invalid date/time values handled: 0
- Rows with invalid numeric values normalized: 0

## Cleaning decisions
- Standardized platform names and mapped common aliases to the project schema.
- Converted date and time values to consistent datetime formats.
- Treated invalid numeric fields as missing and converted them to numeric values.
- Preserved the raw source file while exporting the cleaned dataset to `data/processed/social_media_cleaned.csv`.
- Kept optional fields such as campaign or hashtags when available, and handled missing values gracefully.
