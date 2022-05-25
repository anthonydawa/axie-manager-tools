from transfers import AxieTransferManager
import logging
import os




def check_file(file):
    if not os.path.isfile(file):
        logging.critical('Please provide a correct path to the file. '
                         f'Path provided: {file}')
        return False
    return True

def run_transfer():
    print('working 1')
    # Make Axie Transfers
    logging.info('I shall send axies around')
    # secure = args.get("--safe-mode", None)
    atm = AxieTransferManager('transfers.json', 'secrets_files.json')
    atm.verify_inputs()
    atm.prepare_transfers()
    print('working 2')

run_transfer()
