from enum import Enum


class Actions:
    LIST = "list"
    RETRIEVE = "retrieve"
    CREATE = "create"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    DESTROY = "destroy"


class ReactionTypes(Enum):
    LIKE = "LK"
    DISLIKE = "DS"
    FIRE = "FR"
    HEART = "HR"
    CRY = "CR"
    MINDBLOWING = "MB"
    NUMB = "NB"
    CLOWN = "CL"
    VOMIT = "VM"
