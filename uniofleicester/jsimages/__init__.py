from Products.validation.config import validation
from validators import LinkValidator

# registers validators
validation.register(LinkValidator('isLink'))
