"""Model registry for Alembic autogenerate."""

# Import all models so Base.metadata is populated.
from app.models.user import User  # noqa: F401
from app.models.profile import Profile  # noqa: F401
from app.models.post import Post  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.product import Product  # noqa: F401
