#!c:\users\arnol\code\entroprise-api\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'watchdog==0.10.3','console_scripts','watchmedo'
__requires__ = 'watchdog==0.10.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('watchdog==0.10.3', 'console_scripts', 'watchmedo')()
    )
