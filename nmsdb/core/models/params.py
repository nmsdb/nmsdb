from typing import Type, TypeVar, Union, Any, Optional
from pydantic import BaseModel, Field, create_model
from sqlmodel import SQLModel

from sqlmodel.sql.expression import Select, SelectOfScalar

ModelType = TypeVar("ModelType", bound=SQLModel)


class QueryParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    skip: int = Field(0, ge=0)

    def build_query_params_model(
        base_model: Type[SQLModel],
        *,
        model_name_suffix: str = "QueryParams",
        base_query_params: dict[str, tuple[Any, Any]] = {
            "limit": (int, Field(100, gt=0, le=100)),
            "skip": (int, Field(0, ge=0)),
            "order_by": (str, "created_at"),
        },
        base_class: Type[SQLModel] = SQLModel,
    ) -> Type[SQLModel]:
        fields = {}

        for name, model_field in base_model.model_fields.items():
            field_type = Optional[model_field.annotation]
            default = None
            metadata = model_field.json_schema_extra or {}
            fields[name] = (field_type, Field(default, **metadata))

        # Add limit/skip/order_by
        fields.update(base_query_params)

        # Dynamically generate a new Pydantic model class
        return create_model(
            f"{base_model.__name__}{model_name_suffix}",
            **fields,
            __base__=base_class,
        )

    def apply_to_query(
        self, query: Select | SelectOfScalar, model: Type[ModelType]
    ) -> Union[Select, SelectOfScalar]:
        """
        Apply filters from this params object to a SQLModel select query.

        Args:
            query: The select query to apply filters to
            model: The model class the query is selecting

        Returns:
            The modified query with all filters applied
        """
        for field_name, field_value in self.model_dump(
            exclude={"skip", "limit"}
        ).items():
            if field_value is None:
                continue

            try:
                model_field = getattr(model, field_name)
            except AttributeError:
                continue

            # If value is a dict, assume operator(s); else, default to equality
            if isinstance(field_value, dict):
                for op, op_value in field_value.items():
                    if op_value is None:
                        continue
                    if op == "eq":
                        query = query.where(model_field == op_value)
                    elif op == "ne":
                        query = query.where(model_field != op_value)
                    elif op == "gt":
                        query = query.where(model_field > op_value)
                    elif op == "lt":
                        query = query.where(model_field < op_value)
                    elif op == "ge":
                        query = query.where(model_field >= op_value)
                    elif op == "le":
                        query = query.where(model_field <= op_value)
                    elif op == "contains":
                        query = query.where(model_field.contains(op_value))
                    elif op == "startswith":
                        query = query.where(model_field.startswith(op_value))
                    elif op == "endswith":
                        query = query.where(model_field.endswith(op_value))
                    elif op == "in_":
                        query = query.where(model_field.in_(op_value))
            else:
                # Default to equality if it's not a dict of operators
                if field_value:
                    query = query.where(model_field == field_value)

        return query.offset(self.skip).limit(self.limit)
