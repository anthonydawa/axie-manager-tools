from payments import AxiePaymentsManager
import logging
import os
import sys


def run_payout():
    os.makedirs('logs', exist_ok=True)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

                    
    apm = AxiePaymentsManager('payments.json', 'secrets_files.json', auto='--yes')
    apm.verify_inputs()
    apm.prepare_payout()