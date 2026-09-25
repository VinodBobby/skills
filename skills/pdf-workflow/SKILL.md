---
name: pdf-workflow
description: Read, create, inspect, or make authorized edits to PDF files, including page-level review and form work. Use when the requested result depends on PDF content or layout.
---

# Purpose

Produce or analyze a PDF while preserving page content, order, and visual integrity.

# Workflow

1. Identify the task: extract text, inspect pages, create a PDF, modify pages, or fill a form. Confirm the source file and requested output.
2. For analysis, combine text extraction with page rendering when layout, tables, figures, handwriting, or scanned text matters. Treat OCR output as uncertain until checked against the page image.
3. For edits, preserve page size, orientation, order, links, and form fields unless the user asks to change them. Make only authorized changes.
4. Reopen or render the output. Check affected pages for clipped, missing, duplicated, or obscured content and confirm the file remains readable.
5. Return the PDF or extracted result and state any pages or elements that could not be verified.

# Requirements

Use the PDF tools available in the current environment. Scanned PDFs may need OCR. If page rendering or OCR is unavailable, state the limit rather than claiming visual verification.
