# tests/test_client_example.py

import sys
import os
from typing import Optional, Any

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from poe_ninja_client import (
        PoENinja,
        PoeNinjaRequestError,
        PoeNinjaAPIError,
        CurrencyOverviewResponse,
        ItemOverviewResponse,
        ItemLine,
        CurrencyLine,
        JsonObject,
        CurrencyType,  # New import
        ItemType,  # New import
    )
except ImportError as e:
    print(
        f"ImportError: {e}. Make sure the poe_ninja_client package is installed or PYTHONPATH is set correctly."
    )
    print(
        "If running directly, ensure 'src' directory is in sys.path (attempted above)."
    )
    sys.exit(1)


def run_example():
    """
    Runs the example usage of the PoENinja client.
    """
    try:
        current_league: str = "Settlers"

        if not current_league:
            print(
                "Error: League name is not set. Please update 'current_league' in this script."
            )
            return

        print(f"--- Running PoENinja Client Example for League: {current_league} ---")

        with PoENinja(league=current_league) as client:
            # --- Currency Overview Example ---
            print(
                f"\nFetching '{CurrencyType.CURRENCY.value}' type data for {client.league} league..."
            )
            currency_overview: CurrencyOverviewResponse = client.get_currency_overview(
                currency_type=CurrencyType.CURRENCY
            )

            print(f"\nFound {len(currency_overview.lines)} currency items.")
            print("Displaying first 2 (if available):")
            for c_line in currency_overview.lines[:2]:
                print(
                    f"  Currency: {c_line.currencyTypeName}, Chaos Equivalent: {c_line.chaosEquivalent}"
                )
                if c_line.receive:
                    print(
                        f"    Receive Value (e.g., for 1 Divine): {c_line.receive.value}"
                    )

            # --- Item Overview Example (UniqueWeapon) ---
            item_category_to_test = ItemType.UNIQUE_WEAPON
            print(
                f"\nFetching '{item_category_to_test.value}' data for {client.league} league..."
            )
            item_data: ItemOverviewResponse = client.get_item_overview(
                item_type=item_category_to_test
            )

            print(
                f"\nFound {len(item_data.lines)} items in '{item_category_to_test.value}'."
            )
            print("Displaying first 2 (if available):")
            for i_line in item_data.lines[:2]:
                print(f"  Item Name: {i_line.name}")
                print(
                    f"    Chaos Value: {i_line.chaosValue if i_line.chaosValue is not None else 'N/A'}"
                )
                print(
                    f"    Divine Value: {i_line.divineValue if i_line.divineValue is not None else 'N/A'}"
                )

            # --- Item Overview Example (SkillGem) ---
            item_category_to_test_gem = ItemType.SKILL_GEM
            print(
                f"\nFetching '{item_category_to_test_gem.value}' data for {client.league} league..."
            )
            gem_data: ItemOverviewResponse = client.get_item_overview(
                item_type=item_category_to_test_gem
            )

            print(
                f"\nFound {len(gem_data.lines)} items in '{item_category_to_test_gem.value}'."
            )
            print("Displaying first 2 Skill Gems (if available):")
            for gem_line in gem_data.lines[:2]:
                print(
                    f"  Gem Name: {gem_line.name} (Variant: {gem_line.variant if gem_line.variant else 'N/A'})"
                )
                print(
                    f"    Chaos Value: {gem_line.chaosValue if gem_line.chaosValue is not None else 'N/A'}"
                )

            # --- New: Find Specific Currency Example ---
            currency_to_find = "Chaos Orb"
            print(
                f"\nSearching for '{currency_to_find}' in '{CurrencyType.CURRENCY.value}' type..."
            )
            chaos_orb: Optional[CurrencyLine] = client.find_currency(
                name=currency_to_find, currency_type=CurrencyType.CURRENCY
            )
            if chaos_orb:
                print(f"  Found '{chaos_orb.currencyTypeName}':")
                print(f"    Chaos Equivalent: {chaos_orb.chaosEquivalent}")
                if chaos_orb.receive:
                    print(
                        f"    Value (receive, e.g. for 1 Divine if this is Chaos): {chaos_orb.receive.value}"
                    )
            else:
                print(f"  '{currency_to_find}' not found.")

            divine_orb: Optional[CurrencyLine] = client.find_currency(
                name="Divine Orb", currency_type=CurrencyType.CURRENCY
            )
            if divine_orb:
                print(f"  Found '{divine_orb.currencyTypeName}':")
                print(f"    Chaos Equivalent: {divine_orb.chaosEquivalent}")
            else:
                print("  'Divine Orb' not found.")

            # --- New: Find Specific Item Example ---
            item_to_find = "The Squire"
            item_type_for_find = (
                ItemType.UNIQUE_ARMOUR
            )  # The Squire is a Shield, which falls under UniqueArmour
            print(
                f"\nSearching for '{item_to_find}' in '{item_type_for_find.value}'..."
            )
            found_item: Optional[ItemLine] = client.find_item(
                name=item_to_find, item_type=item_type_for_find
            )
            if found_item:
                print(f"  Found '{found_item.name}':")
                print(
                    f"    Chaos Value: {found_item.chaosValue if found_item.chaosValue is not None else 'N/A'}"
                )
                print(
                    f"    Divine Value: {found_item.divineValue if found_item.divineValue is not None else 'N/A'}"
                )
            else:
                print(f"  '{item_to_find}' not found in '{item_type_for_find.value}'.")

            item_to_find_fail = "Mageblood"
            item_type_for_fail_search = (
                ItemType.UNIQUE_WEAPON
            )  # Mageblood is a belt (UniqueAccessory or UniqueArmour)
            print(
                f"\nSearching for '{item_to_find_fail}' in '{item_type_for_fail_search.value}' (expected fail)..."
            )
            found_item_fail: Optional[ItemLine] = client.find_item(
                name=item_to_find_fail, item_type=item_type_for_fail_search
            )
            if found_item_fail:
                print(
                    f"  Found '{found_item_fail.name}' unexpectedly in '{item_type_for_fail_search.value}'."
                )
            else:
                print(
                    f"  '{item_to_find_fail}' not found in '{item_type_for_fail_search.value}', as expected."
                )

        print("\n--- Example Run Finished ---")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except PoeNinjaRequestError as e:
        print(f"Request Error: {e} (Status Code: {e.status_code})")
    except PoeNinjaAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    run_example()
