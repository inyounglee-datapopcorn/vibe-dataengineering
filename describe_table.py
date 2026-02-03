from google.cloud import bigquery
import json

client = bigquery.Client()
table_ref = "popcorn-vibecoding.toss.meal_service_diet_info"

try:
    table = client.get_table(table_ref)
    
    schema_info = []
    for field in table.schema:
        schema_info.append({
            "name": field.name,
            "type": field.field_type,
            "mode": field.mode,
            "description": field.description
        })
    
    info = {
        "table_id": table.full_table_id,
        "num_rows": table.num_rows,
        "creation_time": str(table.created),
        "last_modified_time": str(table.modified),
        "schema": schema_info
    }
    print(json.dumps(info, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
