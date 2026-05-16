# visualisation_timeline_clean.py

import matplotlib.pyplot as plt
import numpy as np
import os

from geschichte_daten import tabak_daten


def create_clean_vertical_timeline(
    save_path='tabak_timeline.png',
    show_plot=True,
    figsize=(16, 20)
):
    """
    ЧИТАЕМАЯ вертикальная timeline без наложений
    """

    # -------------------------
    # ГРУППИРОВКА ДАННЫХ
    # -------------------------

    events_by_year = {}

    for jahr, kategorie, beschreibung in tabak_daten:

        if jahr not in events_by_year:
            events_by_year[jahr] = []

        events_by_year[jahr].append(
            (kategorie, beschreibung)
        )

    jahre = sorted(events_by_year.keys())

    # -------------------------
    # ЦВЕТА
    # -------------------------

    category_colors = {
        'Werbeverbot': '#E74C3C',
        'Steuererhöhung': '#F39C12',
        'Warnhinweise': '#F1C40F',
        'Jugendschutz': '#2ECC71',
        'Nichtraucherschutz': '#3498DB',
        'Produktregulierung': '#9B59B6',
    }

    # -------------------------
    # FIGURE
    # -------------------------

    fig, ax = plt.subplots(figsize=figsize)

    # Центральная линия timeline
    ax.axvline(
        x=0,
        color='black',
        linewidth=2.5,
        zorder=1
    )

    current_y = 0

    # -------------------------
    # СОБЫТИЯ
    # -------------------------

    for jahr in jahre:

        events = events_by_year[jahr]

        # YEAR LABEL
        ax.text(
            0,
            current_y + 0.8,
            str(jahr),
            fontsize=14,
            fontweight='bold',
            ha='center',
            va='center',
            bbox=dict(
                boxstyle='round,pad=0.3',
                facecolor='white',
                edgecolor='black',
                linewidth=1
            )
        )

        # EVENTS
        for idx, (kategorie, beschreibung) in enumerate(events):

            color = category_colors.get(
                kategorie,
                '#7F8C8D'
            )

            # LEFT / RIGHT
            side = -1 if idx % 2 == 0 else 1

            x_text = side * 3.5

            # DOT
            ax.scatter(
                0,
                current_y,
                s=180,
                color=color,
                edgecolors='black',
                linewidth=1.5,
                zorder=3
            )

            # SHORT TEXT
            short_desc = (
                beschreibung[:55] + '...'
                if len(beschreibung) > 55
                else beschreibung
            )

            # CONNECTION LINE
            ax.plot(
                [0, x_text * 0.92],
                [current_y, current_y],
                color=color,
                linewidth=1.2,
                alpha=0.8
            )

            # TEXT BOX
            ax.text(
                x_text,
                current_y,
                f"{kategorie}\n{short_desc}",
                fontsize=9,
                ha='left' if side > 0 else 'right',
                va='center',
                bbox=dict(
                    boxstyle='round,pad=0.4',
                    facecolor=color,
                    alpha=0.15,
                    edgecolor=color,
                    linewidth=1
                )
            )

            # NEXT EVENT
            current_y -= 1.2

        # GAP BETWEEN YEARS
        current_y -= 0.8

    # -------------------------
    # FORMAT
    # -------------------------

    ax.set_xlim(-5, 5)

    ax.set_ylim(current_y - 1, 2)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # TITLE
    ax.set_title(
        'Tabakprävention in Deutschland\nChronologische Zeitleiste (2000–2023)',
        fontsize=20,
        fontweight='bold',
        pad=25
    )

    # LEGEND
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(
            facecolor=color,
            label=kat,
            alpha=0.7
        )
        for kat, color in category_colors.items()
    ]

    ax.legend(
        handles=legend_elements,
        loc='upper right',
        fontsize=10,
        frameon=True
    )

    # STATS
    stats = (
        f"{len(tabak_daten)} Maßnahmen | "
        f"{len(jahre)} Jahre"
    )

    ax.text(
        0.02,
        0.98,
        stats,
        transform=ax.transAxes,
        fontsize=10,
        va='top',
        bbox=dict(
            boxstyle='round,pad=0.3',
            facecolor='lightgray',
            alpha=0.5
        )
    )

    plt.tight_layout()

    # SAVE
    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches='tight'
    )

    print(f"✅ Gespeichert: {save_path}")

    if show_plot:
        plt.show()
    else:
        plt.close()

    return fig


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":

    create_clean_vertical_timeline(
        save_path='tabak_timeline.png',
        show_plot=True
    )