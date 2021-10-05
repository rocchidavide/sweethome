class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_dot_title(action, dot_name):
    print(f'\n{Colors.OKBLUE}> {action.title()} dot "{dot_name}"{Colors.ENDC}')


def print_row_group(description):
    print(f"\n  {Colors.OKCYAN}  {description}{Colors.ENDC}")


def print_row_status(description, status):
    print(f"    {(str(description) + ' ').ljust(100, '.')} [ {status} ]")
