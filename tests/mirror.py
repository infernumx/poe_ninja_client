# get_mirror_price.py

import sys
import os
from typing import Optional

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from poe_ninja_client import (
        PoENinja,
        CurrencyType,
        CurrencyLine,
        PoeNinjaRequestError,
        PoeNinjaAPIError,
    )
except ImportError as e:
    print(
        f"ImportError: {e}. \nPlease ensure the poe_ninja_client package is in your PYTHONPATH or installed."
    )
    print(
        "If running from the project root, make sure your 'src' directory is structured correctly (e.g., src/poe_ninja_client)."
    )
    sys.exit(1)


def get_mirror_price_in_chaos_and_divine(league: str):
    """
    Fetches the price of a Mirror of Kalandra in Chaos and Divine Orbs for a given league.
    """
    print(f"Attempting to fetch Mirror of Kalandra price for league: {league}")
    try:
        with PoENinja(league=league) as client:
            # 1. Find Mirror of Kalandra
            mirror_name = "Mirror of Kalandra"
            print(
                f"\nSearching for '{mirror_name}' in {CurrencyType.CURRENCY.value}..."
            )
            mirror_data: Optional[CurrencyLine] = client.find_currency_line(
                name=mirror_name, currency_type=CurrencyType.CURRENCY
            )

            if not mirror_data:
                print(
                    f"'{mirror_name}' not found in the {CurrencyType.CURRENCY.value} category for the league '{league}'."
                )
                return

            mirror_chaos_value = mirror_data.chaosEquivalent
            print(f"\n--- {mirror_name} ---")
            print(f"Value in Chaos Orbs: {mirror_chaos_value:,.2f}")

            # 2. Find Divine Orb to calculate Mirror's value in Divines
            divine_orb_name = "Divine Orb"
            print(
                f"\nSearching for '{divine_orb_name}' to determine its Chaos value..."
            )
            divine_orb_data: Optional[CurrencyLine] = client.find_currency_line(
                name=divine_orb_name, currency_type=CurrencyType.CURRENCY
            )

            if not divine_orb_data:
                print(
                    f"'{divine_orb_name}' not found. Cannot calculate Mirror value in Divine Orbs."
                )
                return

            divine_chaos_value = divine_orb_data.chaosEquivalent
            if divine_chaos_value is None or divine_chaos_value == 0:
                print(
                    f"Chaos equivalent for '{divine_orb_name}' is missing or zero. Cannot calculate Mirror value in Divine Orbs."
                )
                return

            print(
                f"Current value of 1 Divine Orb: {divine_chaos_value:,.2f} Chaos Orbs"
            )

            # 3. Calculate Mirror value in Divine Orbs
            mirror_divine_value = mirror_chaos_value / divine_chaos_value
            print(f"Calculated value in Divine Orbs: {mirror_divine_value:,.2f}")
    except (
        ValueError
    ) as ve:  # e.g. if league is empty, though PoENinja init should catch this
        print(f"Configuration Error: {ve}")
    except PoeNinjaRequestError as e:
        print(f"API Request Error: {e} (Status Code: {e.status_code})")
    except PoeNinjaAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # --- Configuration ---
    # !!! IMPORTANT: Replace "Settlers" with the actual current league name !!!
    # You can find active league names on poe.ninja or Path of Exile's official site.
    # If "Settlers" is not an active league with data, this script will likely fail to find items.
    target_league = "Settlers"
    # target_league = "YOUR_CURRENT_LEAGUE_NAME_HERE" # <--- UNCOMMENT AND SET THIS

    if target_league == "Settlers" or target_league == "YOUR_CURRENT_LEAGUE_NAME_HERE":
        print(
            "Warning: Please update 'target_league' with the actual current Path of Exile league name for accurate results."
        )
        # Forcing a known league that might have data for demonstration if "Settlers" is too old.
        # This is just for testing; in a real application, you'd get the league dynamically or from user input.
        # If "Standard" is also not good, you'll need a recent challenge league name.
        # target_league = "Standard" # Fallback for testing, but prices can be very different.
        # print(f"Using fallback league '{target_league}' for demonstration. Update for current league data.")

    get_mirror_price_in_chaos_and_divine(target_league)
