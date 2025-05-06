# src/poe_ninja_client/enums.py
from enum import Enum


class CurrencyType(str, Enum):
    """
    Enum for poe.ninja currency overview types.
    Values correspond to the 'type' query parameter for the currencyoverview endpoint
    and the 'type' parameter for the currencyhistory endpoint.
    """

    # Core Currency
    CURRENCY = "Currency"
    FRAGMENT = "Fragment"

    # Map Related
    SCARAB = "Scarab"
    DELIRIUM_ORB = "DeliriumOrb"
    INVITATION = "Invitation"

    # Crafting Currency
    ESSENCE = "Essence"
    FOSSIL = "Fossil"
    RESONATOR = "Resonator"
    OIL = "Oil"
    CATALYST = "Catalyst"
    VIAL = "Vial"
    INCUBATOR = "Incubator"
    OMEN = "Omen"
    TATTOO = "Tattoo"
    COFFIN = "Coffin"  # Itemized Corpses from Necropolis


class ItemType(str, Enum):
    """
    Enum for poe.ninja item overview types.
    Values correspond to the 'type' query parameter for the itemoverview endpoint
    and the 'type' parameter for the itemhistory endpoint.
    """

    # From user list & previous additions
    UNIQUE_IDOL = "UniqueIdol"
    KALGUURAN_RUNE = "KalguuranRune"
    TATTOO = "Tattoo"
    OMEN = "Omen"
    ARTIFACT = "Artifact"
    OIL = "Oil"
    INCUBATOR = "Incubator"
    UNIQUE_TINCTURE = "UniqueTincture"
    DELIRIUM_ORB = "DeliriumOrb"
    INVITATION = "Invitation"
    SCARAB = "Scarab"
    MEMORY = "Memory"
    FOSSIL = "Fossil"
    RESONATOR = "Resonator"
    ESSENCE = "Essence"
    VIAL = "Vial"

    UNIQUE_WEAPON = "UniqueWeapon"
    UNIQUE_ARMOUR = "UniqueArmour"
    UNIQUE_ACCESSORY = "UniqueAccessory"
    UNIQUE_FLASK = "UniqueFlask"
    UNIQUE_JEWEL = "UniqueJewel"
    UNIQUE_RELIC = "UniqueRelic"
    UNIQUE_MAP = "UniqueMap"

    SKILL_GEM = "SkillGem"
    AWAKENED_GEM = "AwakenedGem"
    TRANSFIGURED_GEM = "TransfiguredGem"

    MAP = "Map"
    BLIGHTED_MAP = "BlightedMap"
    BLIGHT_RAVAGED_MAP = "BlightRavagedMap"

    WATCHSTONE = "Watchstone"

    BASE_TYPE = "BaseType"
    HELMET_ENCHANT = "HelmetEnchant"
    DIVINATION_CARD = "DivinationCard"
    ABYSS_JEWEL = "AbyssJewel"
    CLUSTER_JEWEL = "ClusterJewel"
    CAPTURED_BEAST = "Beast"
    POTION = "Potion"

    HEIST_CONTRACT = "Contract"
    HEIST_BLUEPRINT = "Blueprint"
    HEIST_TARGET = "HeistTarget"
    HEIST_TOOL = "HeistTool"
    HEIST_CLOAK = "HeistCloak"
    HEIST_BROOCH = "HeistBrooch"
    HEIST_GEAR = "HeistGear"


# GraphId Enum has been removed as it's not used by currencyhistory or itemhistory
# based on the latest information.
