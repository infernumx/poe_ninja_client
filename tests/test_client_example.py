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
        CurrencyHistoryResponse,
        ItemHistoryResponse,
        PoeNinjaHistoryDataPoint,  # Updated imports
        ItemLine,
        CurrencyLine,
        CurrencyDetail,
        JsonObject,
        CurrencyType,
        ItemType,  # GraphId removed
    )
except ImportError as e:
    print(f"ImportError: {e}. Ensure package is installed or PYTHONPATH is correct.")
    sys.exit(1)


def run_example():
    try:
        current_league: str = "Settlers"

        if not current_league:
            print("Error: League name must be provided for client initialization.")
            return

        print(f"--- Running PoENinja Client Example for League: {current_league} ---")

        with PoENinja(league=current_league) as client:
            # --- Currency Overview Example ---
            # ... (overview examples can remain similar) ...

            # --- Corrected Currency History Endpoint Example (Divine Orb) ---
            currency_name_for_history = "Divine Orb"
            currency_type_for_history_lookup = CurrencyType.CURRENCY

            print(
                f"\nFetching numeric ID for '{currency_name_for_history}' using type '{currency_type_for_history_lookup.value}'..."
            )
            divine_orb_numeric_id: Optional[int] = client.get_currency_id_by_name(
                currency_name_for_history,
                overview_type=currency_type_for_history_lookup,
            )

            if divine_orb_numeric_id is not None:
                print(
                    f"Found numeric ID for {currency_name_for_history}: {divine_orb_numeric_id}"
                )
                print(
                    f"Fetching history for '{currency_name_for_history}' (ID: {divine_orb_numeric_id}, Type: {currency_type_for_history_lookup.value})..."
                )
                try:
                    divine_history: CurrencyHistoryResponse = (
                        client.get_currency_history(  # Now CurrencyHistoryResponse
                            currency_type_for_history=currency_type_for_history_lookup,
                            currency_id=divine_orb_numeric_id,
                        )
                    )
                    print(
                        f"  Found {len(divine_history.receive_currency_graph_data)} 'receive' data points for {currency_name_for_history}."
                    )
                    if divine_history.receive_currency_graph_data:
                        latest_receive_point = (
                            divine_history.receive_currency_graph_data[0]
                        )
                        print(
                            f"    Latest 'receive' point: {latest_receive_point.daysAgo} days ago, value: {latest_receive_point.value}"
                        )

                    print(
                        f"  Found {len(divine_history.pay_currency_graph_data)} 'pay' data points for {currency_name_for_history}."
                    )
                    if divine_history.pay_currency_graph_data:
                        latest_pay_point = divine_history.pay_currency_graph_data[0]
                        print(
                            f"    Latest 'pay' point: {latest_pay_point.daysAgo} days ago, value: {latest_pay_point.value}"
                        )

                except PoeNinjaAPIError as e:
                    print(
                        f"  Could not fetch currency history for {currency_name_for_history}: {e}"
                    )
                except Exception as einner:
                    print(
                        f"  An unexpected error occurred fetching {currency_name_for_history} currency history: {einner}"
                    )
            else:
                print(
                    f"Could not find numeric ID for '{currency_name_for_history}'. Cannot fetch currency history."
                )

            # --- Corrected Item History Endpoint Example (The Squire) ---
            item_name_for_history = "The Squire"
            item_type_for_history_lookup = ItemType.UNIQUE_ARMOUR

            print(
                f"\nFetching numeric ID for '{item_name_for_history}' using type '{item_type_for_history_lookup.value}'..."
            )
            squire_numeric_id: Optional[int] = client.get_item_id_by_name(
                item_name=item_name_for_history, item_type=item_type_for_history_lookup
            )

            if squire_numeric_id is not None:
                print(
                    f"Found numeric ID for {item_name_for_history}: {squire_numeric_id}"
                )
                print(
                    f"Fetching history for '{item_name_for_history}' (ID: {squire_numeric_id}, Type: {item_type_for_history_lookup.value})..."
                )
                try:
                    squire_history: ItemHistoryResponse = (
                        client.get_item_history(  # Uses ItemHistoryResponse
                            item_type_for_history=item_type_for_history_lookup,
                            item_id=squire_numeric_id,
                        )
                    )
                    print(
                        f"  Found {len(squire_history.data_points)} historical data points for {item_name_for_history}."
                    )
                    if squire_history.data_points:
                        print(
                            f"  Example point: {squire_history.data_points[0].daysAgo} days ago, value: {squire_history.data_points[0].value}"
                        )
                except PoeNinjaAPIError as e:
                    print(
                        f"  Could not fetch item history for {item_name_for_history}: {e}"
                    )
                except Exception as einner:
                    print(
                        f"  An unexpected error occurred fetching {item_name_for_history} item history: {einner}"
                    )
            else:
                print(
                    f"Could not find numeric ID for '{item_name_for_history}'. Cannot fetch item history."
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
