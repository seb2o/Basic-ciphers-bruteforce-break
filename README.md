Simple python functions for alphabetical cipher analysis; frequencies, digram, trigram plot, substitution solving with automated table, viginere solving with key length as input

For the Hill part, it assumes the key matrix is 2*2. With this you can bruteforce all the probable
keys based on the frequent quadgrams, and see if the key decrypts the cipher in readable english

functions to break ceasar cipher, permuation cipher, viginere of key length 5 and Hill cipher of key length 4

To Do : add a cost function on letters frequencies to be able to guess from a string if its distribution
match another distribution to automate the identification process above
