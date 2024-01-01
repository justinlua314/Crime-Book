from menu import Menu, Option

menu_home = Menu(
    "Activities", "What would you like to do", [
        Option("Commit Crime", "menu_crime", 'c'),
        Option("Manage Territory", "menu_territory", 't'),
        Option("Shopping", "menu_shopping", 's'),
        Option("Visit Warehouse", "menu_warehouse", 'w'),
        Option("Inspect Crew Members", "menu_crew", 'i'),
        Option("Recruit new Members", "menu_recruit", 'r')
    ], True
)
