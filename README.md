# ECE-470-Client-Server-SimpleChat
This simple program allows one server and one client to communicate on a turn-based approach using TCP.

The solution was accomplished using a single message class on the server and client side (identical classes). The attributes include the time, alias, and message. The methods include constructing the message to be sent which returns a string, and deconstructing the message that was received to be printed.

The format of the message is: size(bytes):time:alias:message

The size of the message was received as the first four bytes and converted into an int in order to read the rest of the incoming message. If one of the users enters “bye”, the loop will be broken and the protocol will stop. The UTC time had to be formatted in order to ensure that there was a successful conversion to an integer by removing non-integer characters that came standard with the function. It was also formatted in order to be printed in a user friendly way. The alias could also be changed to whatever the user likes as the program will adapt to varying lengths of the alias upon execution. The message can be up to 999 character long including the colons for the time and alias formatting as well as the actual time and alias themselves. 
