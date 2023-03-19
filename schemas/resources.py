from voluptuous import Schema, PREVENT_EXTRA


resource_data = Schema(
                {
                    "id": int,
                    "name": str,
                    "year": int,
                    "color": str,
                    "pantone_value": str
                },
                required=True,
                extra=PREVENT_EXTRA
)

resource_support = Schema(
                {
                    "url": str,
                    "text": str
                },
                required=True,
                extra=PREVENT_EXTRA
)

single_resource_schema = Schema(
                    {
                        "data": resource_data,
                        "support": resource_support
                    },
                    required=True,
                    extra=PREVENT_EXTRA
)

list_resource_schema = Schema(
                    {
                        "page": int,
                        "per_page": int,
                        "total": int,
                        "total_pages": int,
                        "data": [resource_data],
                        "support": resource_support
                    },
                    required=True,
                    extra=PREVENT_EXTRA
)