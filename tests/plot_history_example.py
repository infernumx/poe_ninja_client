# plot_history_example.py

import sys
import os
from typing import Optional, List

# Adjust path to find the poe_ninja_client package if not installed
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from poe_ninja_client import (
        PoENinja,
        ItemType,
        CurrencyType,
        CurrencyHistoryResponse,
        ItemHistoryResponse,
        PoeNinjaHistoryDataPoint,
        PoeNinjaRequestError,
        PoeNinjaAPIError,
    )
except ImportError as e:
    print(
        f"ImportError: {e}. \nPlease ensure the poe_ninja_client package is in your PYTHONPATH or installed."
    )
    sys.exit(1)

try:
    import plotext as plt
except ImportError:
    print(
        "The 'plotext' library is not installed. Please install it to run this example:"
    )
    print("  pip install plotext")
    sys.exit(1)


def plot_terminal_graph(
    data_points: List[PoeNinjaHistoryDataPoint],
    title: str,
    y_label: str = "Value (e.g., Chaos Orbs)",
):
    """
    Plots historical data points in the terminal using plotext.
    Assumes data_points are sorted with the most recent (smallest daysAgo) first.
    """
    if not data_points:
        print(f"No data points to plot for {title}.")
        return

    # plotext plots x from left to right. 'daysAgo' is 0 for today, 6 for a week ago.
    # We want to show time progressing, so we can either:
    # 1. Plot 'daysAgo' directly, and the x-axis represents "days before today".
    # 2. Reverse the order of data so that the oldest data is on the left.
    # Let's use option 1 and label the x-axis accordingly.
    # For plotext, it's often easier if the x-values are numerically increasing left-to-right.
    # So, we'll transform 'daysAgo' to be 'day_index' (0 for oldest, 6 for newest).

    # Sort by daysAgo ascending to have oldest data first for plotting
    sorted_points = sorted(data_points, key=lambda p: p.daysAgo, reverse=True)

    # x_values: 0, 1, 2, ... (representing days from oldest to newest point)
    # x_labels: The actual 'daysAgo' values for ticks
    x_values = list(range(len(sorted_points)))
    y_values = [p.value for p in sorted_points]

    # Create x-axis tick labels based on 'daysAgo'
    # We'll show a few representative labels.
    x_ticks_positions = []
    x_ticks_labels = []
    if len(sorted_points) > 0:
        # Add first, middle (if distinct), and last 'daysAgo' as labels
        x_ticks_positions.append(0)  # Oldest
        x_ticks_labels.append(f"{sorted_points[0].daysAgo}d ago")

        if len(sorted_points) > 2:
            mid_idx = len(sorted_points) // 2
            if (
                sorted_points[mid_idx].daysAgo != sorted_points[0].daysAgo
                and sorted_points[mid_idx].daysAgo != sorted_points[-1].daysAgo
            ):
                x_ticks_positions.append(mid_idx)
                x_ticks_labels.append(f"{sorted_points[mid_idx].daysAgo}d ago")

        if (
            len(sorted_points) > 1
            and sorted_points[-1].daysAgo != sorted_points[0].daysAgo
        ):  # Newest (if different from oldest)
            x_ticks_positions.append(len(sorted_points) - 1)
            x_ticks_labels.append(f"{sorted_points[-1].daysAgo}d ago (Today/Recent)")

    plt.clf()  # Clear previous plot data
    plt.plot(
        x_values, y_values, marker="braille"
    )  # Using braille markers for better resolution
    plt.title(title)
    plt.xlabel("Time (Past -> Present)")
    plt.ylabel(y_label)

    if x_ticks_positions:
        plt.xticks(x_ticks_positions, x_ticks_labels)

    plt.show()
    print("\n")  # Add some space after the plot


def main():
    # --- Configuration ---
    # !!! IMPORTANT: Replace "Settlers" with the actual current league name !!!
    target_league = "Settlers"
    # target_league = "YOUR_CURRENT_LEAGUE_NAME_HERE" # <--- UNCOMMENT AND SET THIS

    if target_league == "Settlers" or target_league == "YOUR_CURRENT_LEAGUE_NAME_HERE":
        print(
            "Warning: Please update 'target_league' with the actual current Path of Exile league name for accurate results."
        )
        # target_league = "Standard" # Fallback for testing
        # print(f"Using fallback league '{target_league}' for demonstration. Update for current league data.")

    print(f"--- Plotting Price History for League: {target_league} ---")

    try:
        with PoENinja(league=target_league) as client:

            # 1. Plot Currency History (e.g., Divine Orb)
            currency_name_to_plot = "Divine Orb"
            currency_type_for_id_lookup = CurrencyType.CURRENCY

            print(f"\nFetching numeric ID for '{currency_name_to_plot}'...")
            divine_orb_numeric_id: Optional[int] = client.get_currency_id_by_name(
                currency_name_to_plot, overview_type=currency_type_for_id_lookup
            )

            if divine_orb_numeric_id is not None:
                print(
                    f"Fetching history for '{currency_name_to_plot}' (ID: {divine_orb_numeric_id})..."
                )
                try:
                    divine_history: CurrencyHistoryResponse = (
                        client.get_currency_history(
                            currency_type_for_history=currency_type_for_id_lookup,
                            currency_id=divine_orb_numeric_id,
                        )
                    )

                    if divine_history.receive_currency_graph_data:
                        plot_terminal_graph(
                            divine_history.receive_currency_graph_data,
                            f"{currency_name_to_plot} Price History (Receive Data) - {target_league}",
                            "Value (e.g., Chaos per Divine)",
                        )
                    else:
                        print(
                            f"No 'receive' history data found for {currency_name_to_plot}."
                        )

                    # You can also plot pay_currency_graph_data if relevant
                    # if divine_history.pay_currency_graph_data:
                    #     plot_terminal_graph(
                    #         divine_history.pay_currency_graph_data,
                    #         f"{currency_name_to_plot} Price History (Pay Data) - {target_league}",
                    #         "Value (e.g., Divines per Chaos)"
                    #     )

                except PoeNinjaAPIError as e:
                    print(
                        f"  Could not fetch currency history for {currency_name_to_plot}: {e}"
                    )
            else:
                print(f"Could not find numeric ID for '{currency_name_to_plot}'.")

            # 2. Plot Item History (e.g., The Squire)
            item_name_to_plot = "The Squire"
            item_type_for_id_lookup = (
                ItemType.UNIQUE_ARMOUR
            )  # Shields are under UniqueArmour

            print(f"\nFetching numeric ID for '{item_name_to_plot}'...")
            squire_numeric_id: Optional[int] = client.get_item_id_by_name(
                item_name=item_name_to_plot, item_type=item_type_for_id_lookup
            )

            if squire_numeric_id is not None:
                print(
                    f"Fetching history for '{item_name_to_plot}' (ID: {squire_numeric_id})..."
                )
                try:
                    squire_history: ItemHistoryResponse = client.get_item_history(
                        item_type_for_history=item_type_for_id_lookup,
                        item_id=squire_numeric_id,
                    )
                    if squire_history.data_points:
                        plot_terminal_graph(
                            squire_history.data_points,
                            f"{item_name_to_plot} Price History - {target_league}",
                            "Value (Chaos Orbs, typically)",  # Item history usually shows chaos value
                        )
                    else:
                        print(f"No history data found for {item_name_to_plot}.")
                except PoeNinjaAPIError as e:
                    print(
                        f"  Could not fetch item history for {item_name_to_plot}: {e}"
                    )
            else:
                print(f"Could not find numeric ID for '{item_name_to_plot}'.")

    except ValueError as ve:
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
    main()
