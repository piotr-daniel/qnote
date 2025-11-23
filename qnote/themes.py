from textual.theme import Theme

# When adding a new theme, ensure to add it to the list at the bottom

qnote_theme = Theme(
    name="qnote",
    primary="#0081a7",
    secondary="#4c566a",
    accent="#ff6b35",
    foreground="#fff4e8",
    background="#0C0C0C",
    success="#A3BE8C", #
    warning="#EBCB8B", #
    error="#BF616A",#
    surface="#0C0C0C",
    panel="#0C0C0C",
    dark=True, #
    variables={
        "block-cursor-text-style": "none", #
        "footer-key-foreground": "#ff6b35", #
        "input-selection-background": "#81a1c1 35%", #
    },
)

all_themes = [qnote_theme]