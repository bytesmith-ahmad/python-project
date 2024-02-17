# my_module.py

def setup(logging):
    logging.basicConfig(filename='.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

def sign():
    """Prints the signature for the demo."""
    print("\nCode/demo by Ahmad Al-Jabbouri\n")