from pydantic import BaseModel


class ModelWithDBMixin(BaseModel):
    """Base model with database mixin"""

    pass


class DecodedModel(ModelWithDBMixin):
    """Model with database mixin for decoded data"""

    pass


class EncodedModel(ModelWithDBMixin):
    """Model with database mixin for encoded data"""

    pass
