from menu import Menu, Option

menu_home = Menu(
    "Activities", "What would you like to do", [
        Option("Recruit new Members", "menu_recruit", 'r'),
        Option("Inspect Crew Members", "menu_crew", 'i'),
        Option("Commit Crime", "menu_crime", 'c'),
        Option("Shopping", "menu_shopping", 's'),
        Option("Manage Territory", "menu_territory", 't'),
        Option("Visit Warehouse", "menu_warehouse", 'w'),
        Option("Manage Business", "menu_business", 'b'),
        Option("Manage save file", "menu_save", 'm')
    ], True
)
