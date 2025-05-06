# src/poe_ninja_client/enums.py
from enum import Enum


class CurrencyType(str, Enum):
    """
    Enum for poe.ninja currency overview types.
    Values correspond to the 'type' query parameter.
    """

    CURRENCY = "Currency"
    FRAGMENT = "Fragment"
    # Add other types as needed, e.g., DeliriumOrb, Catalyst, Oil, Incubator, Scarab, Fossil, Essence, Resonator, Vials
    DELIRIUM_ORB = "DeliriumOrb"
    CATALYST = "Catalyst"
    OIL = "Oil"
    INCUBATOR = "Incubator"
    SCARAB = "Scarab"
    FOSSIL = "Fossil"
    ESSENCE = "Essence"
    RESONATOR = "Resonator"
    VIAL = "Vial"
    # Add more based on https://poe.ninja/api/data/getcurrencyoverview?league=Standard&type=Fragment (explore types)


class ItemType(str, Enum):
    """
    Enum for poe.ninja item overview types.
    Values correspond to the 'type' query parameter.
    This list is not exhaustive and should be expanded based on poe.ninja's API.
    """

    # Weapons
    UNIQUE_WEAPON = "UniqueWeapon"  # Covers 1H, 2H Axes, Maces, Swords, Bows, Claws, Daggers, Staves, Wands
    # Armour
    UNIQUE_ARMOUR = (
        "UniqueArmour"  # Covers Body Armours, Boots, Gloves, Helmets, Shields
    )
    # Accessories
    UNIQUE_ACCESSORY = "UniqueAccessory"  # Covers Amulets, Belts, Rings
    UNIQUE_FLASK = "UniqueFlask"
    UNIQUE_JEWEL = "UniqueJewel"
    ABYSS_JEWEL = "AbyssJewel"  # Might be UniqueJewel or a separate category, check API
    CLUSTER_JEWEL = (
        "ClusterJewel"  # Small, Medium, Large, check if distinct types needed
    )

    # Gems
    SKILL_GEM = "SkillGem"  # Covers normal, awakened, alternate quality etc.
    # poe.ninja might have more granular types like "AwakenedGem"

    # Maps & Fragments
    MAP = "Map"
    BLIGHTED_MAP = "BlightedMap"  # Or just "Map" with a variant?
    UNIQUE_MAP = "UniqueMap"
    MAP_FRAGMENT = "MapFragment"  # Often just "Fragment" in currency overview

    # Other categories
    DIVINATION_CARD = "DivinationCard"
    BEAST = "Beast"
    INVITATION = "Invitation"  # E.g. Maven's Invitation
    HELMET_ENCHANT = "HelmetEnchant"
    BASE_TYPE = "BaseType"  # For fetching base item data (e.g. ilvl 86+ bases)
    WATCHSTONE = "Watchstone"
    # Add more based on https://poe.ninja/api/data/getitemoverview?league=Standard&type=UniqueWeapon (explore types)


# Example of how to get all values if needed:
# ALL_CURRENCY_TYPES = [member.value for member in CurrencyType]
# ALL_ITEM_TYPES = [member.value for member in ItemType]
