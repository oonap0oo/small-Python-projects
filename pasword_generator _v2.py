#!/usr/bin/env python3
#
#  pasword_generator _v2.py
#  
#  Copyright 2025 Nap0
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# generate a password of given length containing numbers, upper case letters,
# lower case letters and optionally symbols

# import the random module
import random 

# seed the random generator
random.seed() 

# generate lists containing the upper case letters, lower case letters and numbers
lowercaseletters = [chr(c) for c in range(97,123)]
uppercaseletters = [c.upper() for c in lowercaseletters]
numbers = [str(k) for k in range(0,10)]
symbols = ["+","-","/","*","_","="]

# ask for the length of the password to be generated
print("Pasword generator", "-" * 17, sep = "\n")
answer = input("\nlength of the pasword? ")
addsymbols = input(f"\n Include sympbols like {" ".join(symbols)} ?\n  y or n? ").lower()

# check if a valid number was givin
if answer.isnumeric():
    # convert the length to an integer
    length = int(answer)
    
    # divide the requested number of characters into the different kinds
    if addsymbols == "y":
        Nlower, Nupper, Nsymbols = (length // 4 + 1), (length // 4 ), (length // 4 )
        Nnumber = length - Nlower - Nupper - Nsymbols
    else:
        Nlower, Nupper = (length // 3 + 1), (length // 3)
        Nnumber = length - Nlower - Nupper
    
    # generate a list of  a number of randomnly chosen upper case letters 
    passwordaslist = random.choices(uppercaseletters, k = Nupper)
    
    # add a number of randomnly chosen lower case letters to the list
    passwordaslist.extend( random.choices(lowercaseletters, k = Nlower) )
    
    # add a number of randomnly chosen numbers to the list
    passwordaslist.extend( random.choices(numbers, k = Nnumber) )
    
    # if adding symbols was chosen, add randomly chosen symbols to the list
    if addsymbols == "y":
        passwordaslist.extend( random.choices(symbols, k = Nsymbols) )
    
    # randomly mix elements of the complete list
    random.shuffle(passwordaslist)
    
    # make a string from the elements in the list which are 1 character strings
    password = "".join(passwordaslist)
    
    # get a string woth all the unique characters using a set conversion
    uniquecharacters = "".join(set(passwordaslist)) 
    
    # generate the ouput information
    output = f"\nThe new password:\n\n{password}\n\nhas a length of {len(password)} characters\
    \n{Nupper} upper case letters\n{Nlower} lower case letters\n{Nnumber} numbers"
    if addsymbols == "y":
        output+=f"\n{Nsymbols} symbols"
    output += f"\nIt contains {len(uniquecharacters)} unique characters"
    
    print(output) 
    
else:
    print("\n", answer, "is not a valid length, terminating")
    

