# visualisation_timeline_clean.py
import matplotlib.pyplot as plt
import textwrap
from collections import defaultdict
from geschichte_daten import tabak_daten
import os


# ====================== KONSTANTEN ======================
SAVE_DIR = '__Markt-analyse__/Grafiken'
SAVE_PATH = os.path.join(SAVE_DIR, 'tabak_timeline.png')

FIGSIZE = (19, 23)
DPI = 340

TEXT_OFFSET_BASE = 3.3
TEXT_SCALE = 0.058
POINT_BASE_SIZE = 158
POINT_STEP = 34

EVENT_SPACING = 2.05
YEAR_SPACING = 1.45


def create_clean_vertical_timeline(save_path=SAVE_PATH, show_plot=True):
    """Erstellt eine saubere vertikale Timeline der Tabakpräventionsmaßnahmen"""

    os.makedirs(SAVE_DIR, exist_ok=True)

    events_by_year = defaultdict(list)
    for jahr, kategorie, beschreibung in tabak_daten:
        events_by_year[jahr].append((kategorie, beschreibung))

    jahre = sorted(events_by_year.keys())

    category_colors = {
        'Werbeverbot': '#C44E52',
        'Steuererhöhung': '#DD8452',
        'Warnhinweise': '#CCB974',
        'Jugendschutz': '#55A868',
        'Nichtraucherschutz': '#4C72B0',
        'Produktregulierung': '#8172B2'}
        

    legend_order = ['Werbeverbot', 'Jugendschutz', 'Nichtraucherschutz',
                    'Steuererhöhung', 'Warnhinweise', 'Produktregulierung']
    

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.axvline(x=0, color="#3A3434", linewidth=1.9, zorder=1)

    current_y = 0.0

    for jahr in jahre:
        events = events_by_year[jahr]
        num_events = len(events)

        ax.axhline(current_y + 0.6, color='#aaaaaa', linewidth=0.9, alpha=0.6)
        ax.text(0, current_y + 1.1, str(jahr), fontsize=15, fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.7', facecolor='white',
                          edgecolor='#444444', linewidth=1.1))

        for idx, (kategorie, beschreibung) in enumerate(events):
            color = category_colors.get(kategorie, '#7F8C8D')
            side = -1 if idx % 2 == 0 else 1

            wrapped = textwrap.wrap(beschreibung, width=36)
            short_desc = "\n".join(wrapped)
            max_line_len = max((len(line) for line in wrapped), default=20)

            x_text = side * (TEXT_OFFSET_BASE + max_line_len * TEXT_SCALE)

            point_size = POINT_BASE_SIZE + num_events * POINT_STEP
            ax.scatter(0, current_y, s=point_size, color=color,
                       edgecolors='white', linewidth=2.4, zorder=4)

            ax.plot([0, x_text * 0.92], [current_y, current_y],
                    color='#777777', linewidth=1.1, alpha=0.7, zorder=2)

            ax.text(x_text, current_y, f"{kategorie}\n{short_desc}",
                    fontsize=9.8,
                    ha='left' if side > 0 else 'right',
                    va='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor=color,
                              alpha=0.08, edgecolor=color, linewidth=0.9))

            current_y -= EVENT_SPACING

        current_y -= YEAR_SPACING

    # ==================== FORMATIERUNG ====================
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(current_y - 2, 4.2)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    total = len(tabak_daten)

    ax.set_title('Tabakprävention in Deutschland\n''Gesetzliche Maßnahmen (2000–2023)\n''23 Maßnahmen • 15 Jahre • 6 Kategorien',
        fontsize=19,pad=20)

    # Legende
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=category_colors[k], alpha=0.85, label=k)
                       for k in legend_order]

    ax.legend(handles=legend_elements, loc='lower center',
              bbox_to_anchor=(0.5, -0.07), ncol=3, fontsize=10.8, frameon=False)

    # Quelle
    ax.text(0.5, -0.13,
            "Quelle: Eigene Darstellung nach DKFZ, BZgA und gesetzlichen Regelungen.",
            transform=ax.transAxes, ha='center', fontsize=9.5,
            color='#666666', style='italic')

    plt.tight_layout(pad=3.2)

    plt.savefig(save_path, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"✅ Timeline gespeichert: {save_path}")

    if show_plot:
        plt.show()
    else:
        plt.close()

    return fig


if __name__ == "__main__":
    os.makedirs(SAVE_DIR, exist_ok=True)

    create_clean_vertical_timeline(
        save_path=SAVE_PATH,
        show_plot=True
    )