import os
from tqdm import tqdm
from multiprocessing.dummy import Pool
from src.setup_logger import ConsoleLogger
import argparse
import shutil


def find_wavfiles(path):
    """
    Returns an iterable of all wav files in directory.
    :param path: path to search recursively.
    :return: Iterable with full filepath of wav file.
    """
    logger.info(f"Crawling root directory. This may take some time...")
    wav_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            # append the file name to the list
            if file.endswith('.wav'):
                logger.debug(f"[-] Found WAV file: {file}")
                wav_files.append(os.path.join(root, file))

    return wav_files


def parse_wavfile(wavfile):
    with open(wavfile, 'rb') as f:
        s = f.read()
    if s.find(acid_bytes) != -1:
        logger.success(f"Found Acid Loop WAV format: {wavfile}")
        return wavfile
    else:
        return None


def relocate_wavfile(wavfile):

    if preserve:
        preserve_path = wavfile.replace(root_path, "")
        if not to_path.endswith("/"):
            new_path = to_path + "/" + preserve_path
        else:
            new_path = to_path + preserve_path
        try:
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            shutil.copy(wavfile, new_path)
            logger.debug(f"Relocated {wavfile} to {new_path}")
        except Exception as e:
            logger.error(f"File was not able to be moved! Error: {e}")
    else:
        filename = os.path.basename(wavfile)
        if not to_path.endswith("/"):
            new_path = to_path + "/" + filename
        else:
            new_path = to_path + filename
        try:
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            shutil.copy(wavfile, new_path)
            logger.debug(f"Relocated {wavfile} to {new_path}")
        except Exception as e:
            logger.error(f"File was not able to be moved! Error: {e}")


def relocate_worker(wavfile):
    retn_code = False
    if parse_wavfile(wavfile):
        retn_code = True
        relocate_wavfile(wavfile)

    return retn_code


def main():

    parser = argparse.ArgumentParser('Find Acid Loop WAV files and move them to another directory.')
    # Switched args
    parser.add_argument("-v", dest="verbose", action='count', default=1,
                        help="Enable verbose output. Ex: -v, -vv, -vvv")
    parser.add_argument("--preserve", dest="preserve", action='store_true',
                        help="Preserve folder structure from source path.")
    parser.add_argument("-f", "--from", dest="root_path", action="store", required=True,
                        help="The root path to search for files.")
    parser.add_argument("-t", "--to", dest="to", action="store", required=True,
                        help="The path to copy files to.")

    args = parser.parse_args()
    # Define some globals.
    global acid_bytes
    acid_bytes = b"\x61\x63\x69\x64"
    global vlevel
    vlevel = args.verbose
    global logger
    logger = ConsoleLogger(vlevel)
    global to_path
    to_path = args.to
    if not os.path.exists(to_path):
        logger.warn(f"Path doesn't exist yet. Creating: {to_path}")
        os.mkdir(to_path)
    global root_path
    root_path = args.root_path
    global preserve
    preserve = args.preserve

    # Locate all WAVFiles under directory and subdirectories.
    wavfiles = find_wavfiles(root_path)
    logger.info(f"Found a total of {len(wavfiles)} WAV files. Searching for ACID LOOPs...")
    pbar = tqdm(total=len(wavfiles), unit=" WAV File(s)", maxinterval=0.1, mininterval=0)
    p = Pool(100)
    acidized_file_counter = 0
    for _ in p.imap_unordered(relocate_worker, wavfiles):
        pbar.update()
        if _:
            acidized_file_counter += 1
    logger.info(f"Successfully copied {acidized_file_counter} acidized file(s)!")


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print(f"[!] Error: You must specify the to and from paths. Usage: acidloopmover <from_path> <to_path>")
