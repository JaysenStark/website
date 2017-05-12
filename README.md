# website

This is a python django project built for acpc gui cliet.

It provide gui interface for player to player heads-up limit texas hold'em or heads-up no-limit texas hold'em.

It starts a dealer program (it's from acpc), then start an agent program (AI) to connect to dealer, finally keep 
a socket connection with dealer for human player.
It use matchstate string from dealer program, use this string to reconstruct game state which is observable by 
human player, then return a dict representation of the game state, render the game state on web browser.
It accept actions made by human players from browser, then construct valid response to be sent to dealer.
