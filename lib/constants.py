from enum import Enum

class AccountAttributes(Enum):
    followers = 'followers'
    following = 'following'

class LinkTypes(Enum):
    common = 'common'
    uncommon = 'uncommon'

class GraphLayoutTypes(Enum):
    circular_layout = 'circular_layout'
    spring_layout = 'spring_layout'
    spectral_layout = 'spectral_layout'