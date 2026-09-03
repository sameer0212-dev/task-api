# Job Card: Book Content Enrichment

## 📚 Overview

The **Book Content Enrichment** job processes scraped book records and enriches them with normalized categories, key thematic tags, quality indicators, and a concise one-sentence summary.

---

## 📥 Input

The job accepts a JSON object containing the book's title and description.

```json
{
  "title": "string (1-200 chars)",
  "description": "string (1-3000 chars)"
}
```

### Input Fields

| Field         | Type     | Constraints       | Description              |
| ------------- | -------- | ----------------- | ------------------------ |
| `title`       | `string` | 1–200 characters  | Book title               |
| `description` | `string` | 1–3000 characters | Book description/content |

---

## 📤 Output

The job returns a structured JSON object containing the normalized category, confidence score, themes, summary, and quality flags.

```json
{
  "category": "Fiction",
  "confidence": 0.95,
  "themes": [
    "friendship",
    "adventure"
  ],
  "one_sentence_summary": "A story about friendship and adventure.",
  "quality_flags": []
}
```

### Output Fields

| Field                  | Type            | Description                                        |
| ---------------------- | --------------- | -------------------------------------------------- |
| `category`             | `string`        | Normalized book category                           |
| `confidence`           | `float`         | Confidence score for the selected category         |
| `themes`               | `array[string]` | Key themes identified in the content               |
| `one_sentence_summary` | `string`        | Concise one-sentence summary                       |
| `quality_flags`        | `array[string]` | Issues or quality indicators detected in the input |

---

## 🏷️ Allowed Categories

The `category` field **must** contain exactly one of the following values:

```text
Fiction
Non-Fiction
Academic
Children
Other
```

No other category values are permitted.

---

## 🚫 It Must Never

The enrichment job must **never**:

1. Return a category outside the defined category list.
2. Return plain prose, raw Markdown tags, or unformatted text instead of the required structured JSON output.
3. Hallucinate, invent, or guess personal user data.

---

## 🤔 Uncertainty Handling

When the model cannot confidently determine the appropriate category, it must fall back to:

```json
{
  "category": "Other",
  "confidence": 0.4
}
```

The confidence score **must be below `0.5`** whenever the category is `"Other"` due to uncertainty.

---

## 🎯 Job Requirements

The enrichment pipeline should:

* Normalize book categories.
* Identify meaningful themes.
* Generate a concise one-sentence summary.
* Detect and report relevant quality issues.
* Provide a confidence score for categorization.
* Always return predictable, structured JSON.
* Gracefully handle uncertain or ambiguous content.

---

## 🔒 Output Contract

Every successful enrichment response must conform to the following structure:

```json
{
  "category": "Fiction | Non-Fiction | Academic | Children | Other",
  "confidence": 0.95,
  "themes": ["string"],
  "one_sentence_summary": "string",
  "quality_flags": ["string"]
}
```

The output contract should remain consistent regardless of the book being processed.
