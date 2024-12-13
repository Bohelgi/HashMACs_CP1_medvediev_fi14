from Crypto.Hash import RIPEMD160
import time

ORIGINAL_TEXT = "Medvediev Oleg Evgeniyovich"
SECOND_ORIGINAL_TEXT = "FI-14 Medvediev Oleg Evgeniyovich"
HASH_SUFFIX_LENGTH_PREIMAGE = 4
HASH_SUFFIX_LENGTH_BIRTHDAY = 8 

def ripemd160(msg: str) -> str:
    h = RIPEMD160.new()
    h.update(msg.encode('utf-8'))
    return h.hexdigest()

def preimage_attack(original_text: str):
    print("\nPreimage attack:")
    original_hash = ripemd160(original_text)
    print(f"Original text: {original_text}; Hash: {original_hash}")
    
    start_time = time.time()
    i = 0
    while True:
        new_text = f"{original_text}{i}"
        new_hash = ripemd160(new_text)
        
        if i < 30:
            print(f"Iteration {i}: Text: {new_text}; Hash: {new_hash}")
        
        if new_hash[-HASH_SUFFIX_LENGTH_PREIMAGE:] == original_hash[-HASH_SUFFIX_LENGTH_PREIMAGE:]:
            print(f"Collision found: {new_text}; Hash: {new_hash}")
            print(f"Time: {time.time() - start_time:.2f} seconds")
            print(f"Collision found on iteration: {i}")
            break
        
        i += 1

def birthday_attack(original_text: str):
    print("\nBirthday attack:")
    original_hash = ripemd160(original_text)
    print(f"Original text: {original_text}; Hash: {original_hash}")
    
    hash_dict = {original_text: original_hash}
    
    start_time = time.time()
    i = 0
    while True:
        new_text = f"{original_text}{i}"
        new_hash = ripemd160(new_text)
        
        if i < 30:
            print(f"Iteration {i}: Text: {new_text}; Hash: {new_hash}")
        
        for key, value in hash_dict.items():
            if new_hash[-HASH_SUFFIX_LENGTH_BIRTHDAY:] == value[-HASH_SUFFIX_LENGTH_BIRTHDAY:]:
                print(f"Collision found:\nFirst member:\tText: {key}; Hash: {value}\nSecond member:\tText: {new_text}; Hash: {new_hash}")
                print(f"Time: {time.time() - start_time:.2f} seconds")
                print(f"Collision found on iteration: {i}")
                return
        
        hash_dict[new_text] = new_hash
        i += 1

def main():
    preimage_attack(ORIGINAL_TEXT)
    birthday_attack(SECOND_ORIGINAL_TEXT)

if __name__ == "__main__":
    main()
