from django_enumfield import enum


class OrderStatus(enum.Enum):
    @classmethod
    def invert_label(cls, s):
        return cls.inverted_labels.get(s, 0)


class MarketplaceStatus(OrderStatus):
    NA = 0
    VALIDATED_FIANET = 1
    ACCEPT = 2

    labels = {
        NA: '',
        VALIDATED_FIANET: 'ValidatedFianet',
        ACCEPT: 'accept'
    }

    inverted_labels = {v: k for k, v in labels.iteritems()}


class LengowStatus(OrderStatus):
    NA = 0
    NEW = 1
    PROCESSING = 2
    SHIPPED = 3
    CANCELLED = 4

    labels = {
        NA: '',
        NEW: 'new',
        PROCESSING: 'processing',
        SHIPPED: 'shipped',
        CANCELLED: 'cancel'
    }

    inverted_labels = {v: k for k, v in labels.iteritems()}
