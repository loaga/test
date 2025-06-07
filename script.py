import sys
# Initial sys.path modification might be here or not, subtask is specific
# The following line is necessary to ensure the 'ku' module can be found in the specified path.
# This may need to be adjusted based on the actual location of 'ku.py' in your environment.
sys.path.insert(1, '/home/klai/taibuun/KeSi/kesi/butkian') # Target line
from ku import Ku

#test = ['boeh--m̄', 'Gâu-chá', 'lêng-ngāu', 'góa ê siaⁿ']
test = ['boeh--m̄', 'Gâu-chá', 'lêng-ngāu', 'góa ê siaⁿ', 'sann-chành', 'Thô-kha-á', 'pái-thô', 'Thô-kha-á', 'nng-nng-nng', 'ko-ko-ko', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah', 'kah']

if __name__ == '__main__':
    dbg = False
    for item in test:
        ku_instance = Ku(item)
        mtl_result = ku_instance.MTL(dbg).mtl
        print(f"Original: {item}, MTL: {mtl_result}")
