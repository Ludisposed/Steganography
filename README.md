# Steganography
A python steganography tool

~~*Main TODO*~~
 - [x]  Main funtion to accept argument
 - [x]  A function what reads images and writes it to a byte-array
 - [x]  A Encoder function
 - [x]  A Decoder function

~~*Also TODO*~~
 - [x]  Encrypt the text
 - [x]  Add Code to randomize
     + Example -rgb rb # Changes only Red and Blue
     + Example -s 10   # Steps over 10 rbg arr and then changes~~

~~*New TODO*~~
 - [x]  Add check if image has enough space for the string to hide
 - [x]  Make code more readable for other programmers PEP-8
 - [x]  Make more prints for users
 - [x]  improve seed method
 - [x]  **MAYBE** Add encryption from file... instead of text in command promt

~~*Yet Another TODO*~~
 - [x]  Fake data
 - [x]  Rename as suggested
 - [x]  refractor usability of the code....
   - A python script that drives the command line tool
   - A module that handles LSB encoding/decoding, and operates on an image array. It should make no attempt at encryption, but simply work with whatever data is passed, whether encrypted or not.
   - A separate module to handle encryption/decryption.

*Newest TODO*
 - [ ]  RSA-BASED-ENCRYPTION/DECRYPTION
 - [x]  improve location of files, so we can work with files outside of the current directory
 - [ ]  complete ./install ---> Setup source controll
        Example: 
        
        stego/
        
        |------Setup/Install
        
        |------Test
        
        |------stego
              |--------module1.py
              
              |--------module2.py
              
              |-------- __init__.py
              
