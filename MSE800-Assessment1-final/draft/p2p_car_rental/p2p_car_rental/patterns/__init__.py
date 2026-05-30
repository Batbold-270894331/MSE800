"""Design patterns module."""
from patterns.insurance_strategy import (
    InsuranceStrategy, NoInsurance, BasicInsurance,
    StandardInsurance, PremiumInsurance,
    get_insurance, list_all_insurance,
)

__all__ = [
    'InsuranceStrategy', 'NoInsurance', 'BasicInsurance',
    'StandardInsurance', 'PremiumInsurance',
    'get_insurance', 'list_all_insurance',
]
