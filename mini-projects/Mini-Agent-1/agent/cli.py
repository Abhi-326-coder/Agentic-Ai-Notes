def print_banner():
    """Print an ASCII-only banner that works in legacy Windows consoles."""
    print(
        """
+--------------------------------------+
|             MINI AGENT               |
|          Gemini 2.5 Flash            |
+--------------------------------------+
"""
    )


def print_help():
    print(
        """
Commands:

  /help     Show this help message
  /clear    Clear conversation memory
  /state    Show current agent state
  /tools    Show available tools
  /exit     Exit the program
"""
    )
