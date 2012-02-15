ABOUT

OpenGL Library is a collection of interfaces for dealing with PyOpenGL, stored in the folder "glLib".  See "Documentation.doc" for version details.  
OpenGL Library was made and is maintained by Ian Mallett (ian@geometrian.com; see CONTACT, below, for issues).  
OpenGL Library is released fully open source with the assumption that it may be reused and redistributed under an honor system.  You may redistribute, alter, etc. the code, just so long as you don't claim total responsibility for creating the library in the first place--because that would be, you know, not true.  See Copying.txt.  


RESOURCES

"Function List.doc" is a list of functions for quick syntatical reference.
"Documentation.doc" is a list of these functions with detailed explanations.
"Shaders.doc" shows how to use shaders in OpenGL Library.
"To Do.doc" gives a list of all todo items for OpenGL Library.
"Tips and Tricks.doc" provides a few helpful tricks for squeezing extra performance out of the library and doing other advanced features not mentioned as tutorials.  

The folder "Tutorials" contains Python files showing how to use OpenGL Library to do certain things.  "Tutorial.py" is an interface providing access to all the tutorials at once and is not a tutorial in and of itself.  

A few helpful programs are provided to help development with OpenGL Library.  Both require wxPython.:
"TileTest.py" opens an image and displays it to the screen.  Click and drag to see the edges.  This allows you to visually check to see if that image is tileable.  
"HeightmapToNormalmap.py" changes a heightmap to a tangent space normalmap.  Bumpmapping is not directly supported by OpenGL Library, because extra computation must be done in the shader to change the height data to normal data, slowing the program.  Future versions may change this.  Unless other functions that require height data are being used, such as parallax effects, it is generally faster to pass the normal data directly.  This program converts a heightmap image to its normalmap.


CONTACT

You are free to contact me at ian@geometrian.com for any legitimate reason.  This means if you are having trouble figuring out how to use something, want to talk about the library itself, or simply want a philosophical discussion about cheese.  See SUPPORT, below, for the first two cases.  So, basically, I'm enthusiastic about real communication, but spam me and die.  


SUPPORT

I feel that the documentation and tutorials are extremely good resources for learning how to use OpenGL Library--please only contact me for help if you really can't understand them.  Again, note that moderate to advanced knowledge of OpenGL is essential to using this library.  If you do not know basic concepts, like the rendering pipeline, double buffering, lighting models, you're in over your head trying to implement the advanced features this library provides, no matter how abstracted it makes them.  I'm open to usage help requests, but again, you have to know your stuff and, most importantly, have at least tried to fix the problem yourself.  

Many of the functions available in this library implement advanced effects.  These are currently tested only on a single system, and it is possible (even likely) that a compatibility fix may be in order.  I freely acknowledge my library is almost certainly not perfect.  If you want to see a new feature that's not on the todo list implemented, want to push an item on the todo list for greater priority, report a bug, or if you find any error at all in the documentation, function list or any place in the library itself, don't hesitate to contact me at ian@geometrian.com.  