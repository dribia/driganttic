"""Schema base for data validation results.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

from pydantic import BaseModel


class Base(BaseModel):
    """Schema base for data validation results."""

    class Config:
        """Base Schema configuration class.

        validate_assignment: Validate fields on assignment.

        """

        validate_assignment = True

    def set_attributes(self, **kwargs):
        """Utility method to set various attributes at once.

        Args:
            kwargs: Attributes to set.

        """
        for attr_key, attr_value in kwargs.items():
            setattr(self, attr_key, attr_value)
