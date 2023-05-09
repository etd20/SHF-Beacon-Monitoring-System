# Takes a Morse Code string and decodes it
class CW:
    def __init__(self):
        # Create a dictionary of Morse Code to characters for decoding.
        self.MORSE_CODE_DICT =  {'.-':'A', '-...':'B',
                    '-.-.':'C', '-..':'D', '.':'E',
                    '..-.':'F', '--.':'G', '....':'H',
                    '..':'I', '.---':'J', '-.-':'K',
                    '.-..':'L', '--':'M', '-.':'N',
                    '---':'O', '.--.':'P', '--.-':'Q',
                    '.-.':'R', '...':'S', '-':'T',
                    '..-':'U', '...-':'V', '.--':'W',
                    '-..-':'X', '-.--':'Y', '--..':'Z',
                    '.----':'1', '..---':'2', '...--':'3',
                    '....-':'4', '.....':'5', '-....':'6',
                    '--...':'7', '---..':'8', '----.':'9',
                    '-----':'0', '--..--':',', '.-.-.-':'.',
                    '..--..':'?', '-..-.':'/', '-....-':'-',
                    '-.--.':'(', '-.--.-':')'}

# Decrypt from Morse Code to English Characters
    def decrypt(self, message):
        # Increment space counter
        i=0
        # Create a blank string for the actual message
        decipher = ''
        # Create a blank string for the character elements
        citext = ''
        # Iterate over the CW message
        for letter in message:
            # If the letter is not a space
            if (letter != ' '):
                # Reset space counter
                i = 0
                # Add letter to citext for decoding
                citext += letter
            else:
                # Increment the space counter by one
                i += 1
                # If there are two spaces
                if i == 2 :
                    # Add a space to the final decoded message
                    decipher += ' '
                else:
                    # Add the looked up CW in citext to the deciphered message, if there is no CW that matches, add Error to the string instead
                    decipher += self.MORSE_CODE_DICT.get(citext, "Error")
                    # Clear citext for next set of elements
                    citext = ''
        # Returns final deciphered message as a string
        return decipher