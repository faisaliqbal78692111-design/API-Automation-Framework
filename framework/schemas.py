"""JSON schemas for ReqRes responses, used with jsonschema.validate()."""

USER = {
    "type": "object",
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+$"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string", "pattern": "^https?://"},
    },
}

RESOURCE = {
    "type": "object",
    "required": ["id", "name", "year", "color", "pantone_value"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "year": {"type": "integer"},
        "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
        "pantone_value": {"type": "string"},
    },
}


def page_of(item_schema: dict) -> dict:
    """Schema for a paginated list response whose `data` items match item_schema."""
    return {
        "type": "object",
        "required": ["page", "per_page", "total", "total_pages", "data"],
        "properties": {
            "page": {"type": "integer"},
            "per_page": {"type": "integer"},
            "total": {"type": "integer"},
            "total_pages": {"type": "integer"},
            "data": {"type": "array", "items": item_schema},
        },
    }
