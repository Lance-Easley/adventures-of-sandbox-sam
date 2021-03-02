# Adventures of Sandbox Sam

This is my go at a side-scroller sandbox game.
It is built using the Python module "Pygame", a library of graphics and geometry functions and classes.

## How it works

Currently, there is a single text file (world.txt) which consists of a 64 by 32 array of characters. 
Each character represents a different block in the game, except for `0` which represents an empty "air" block.
When launching the game, the world is generated according to that text file. 

Once the game has loaded, the character is controlled with the keys `a`, for left, `d`, for right, `space` to jump, and using the mouse cursor to interact with the world.
You'll notice that upon loading in, the cursor will have an icon displayed next to it. 
That is your interaction mode. 
If a pickaxe is displayed, you are in mining mode. 
If a block is displayed, you are in building mode.

If you click on a block whie in mining mode, the block will be moved from the world into your hotbar, shown at the bottom of your screen.
If you mine a block that is already in your hotbar, the block will "stack" in the same hotbar slot.
However, if the block is different, that block will occupy a new slot.

In order to properly use build mode, use the number keys to select a hotbar slot.
If you click on an empty "air" block while in build mode and you have a block selected in your hotbar, the block will move from your hotbar to the world.
If your selected hotbar slot has more than one block stacked, then it only takes one block out of the stack.
