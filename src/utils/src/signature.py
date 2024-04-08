def sign() -> str:
    """Returns the signature for the demo.
    Does not print: useful for caching output.
    """
    return str("\n"
          +"\033[1m"  # ANSI for bold style
          +"\033[3m"  # ANSI for italic style
          +"\033[4m"  # ANSI for underline style
          +"\033[5m"  # ANSI for blinking effect
          +"\033[93m" # ANSI for bright yellow
          +"Code/demo by Ahmad Al-Jabbouri"
          +"\033[0m"  # This ANSI escape removes all styles
          +"\n")