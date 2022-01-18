from claims import AxieClaimsManager
import logging
import os
import sys


os.makedirs('logs', exist_ok=True)
log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

acm = AxieClaimsManager('payments.json','secrets_files.json')
acm.verify_inputs()
acm.prepare_claims()
