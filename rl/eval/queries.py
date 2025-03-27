from omegaconf import OmegaConf
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def all_fields():
    return "SELECT * FROM eval_data"

def total_metric(metric_field: str, filters: Dict[str, Any]):
    where_clause = build_where_clause(filters)
    query = f"""
        SELECT
            policy_name,
            eval_name,
            AVG(CAST("{metric_field}" AS DOUBLE)) AS mean_{metric_field.replace('.', '_')},
            STDDEV(CAST("{metric_field}" AS DOUBLE)) AS std_{metric_field.replace('.', '_')}
        FROM eval_data
        {where_clause}
        GROUP BY policy_name, eval_name
        ORDER BY policy_name, eval_name;"""

    return query

def build_where_clause(filters: Dict[str, Any]) -> str:
    """Build WHERE clause from a filters dictionary."""
    if not filters:
        return ""
    conditions = []

    # Convert OmegaConf objects to plain Python types if necessary.
    if OmegaConf.is_config(filters):
        filters = OmegaConf.to_container(filters, resolve=True)

    for field, value in filters.items():
        # If field names contain dots, wrap them in quotes.
        if OmegaConf.is_config(value):
            value = OmegaConf.to_container(value, resolve=True)
        if '.' in field and not field.startswith('"'):
            field = f'"{field}"'
        if field == "policy_name" and len(value) == 1:
            p = value[0].replace("wandb://run/", "")
            conditions.append(f"{field} LIKE '%{str(p)}%'")
        elif isinstance(value, (list, tuple)):
            logger.warning("If filtering by policy name with multiple policies, please include policy version.")
            formatted_values = [f"'{str(v.replace('wandb://run/', ''))}'" for v in value]
            conditions.append(f"{field} IN ({', '.join(formatted_values)})")
        elif isinstance(value, str):
            value = value.strip()
            if value.startswith(('>', '<', '=', '!=', '>=', '<=', 'IN', 'BETWEEN', 'IS')):
                conditions.append(f"{field} {value}")
            else:
                conditions.append(f"{field} = '{value}'")
        else:
            conditions.append(f"{field} = {value}")
    return f"WHERE {' AND '.join(conditions)}" if conditions else ""
