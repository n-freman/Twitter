from pydantic import BaseModel, SecretStr


class BaseSchema(BaseModel):

    def as_args(self):
        results = self.model_dump()
        for key, value in results.items():
            if isinstance(value, SecretStr):
                results[key] = value.get_secret_value()
        return results
