# Concepts
- At the most abstract level, a codebase is made up of a bunch of 'objects'.
    - Objects include files, folders, classes, functions, variables.
    - Objects can be represented using different symbols e.g. File = fileshape, class = Rectangle
- These objects are related to each other in a bunch of different ways. Given two objects A and B, relations include:
    - folder A contains file B
    - file A declares class B
    - file A declares method B
    - method A calls method B
    - method A isCalledAfter method B in method C
    - classInstance A isInstanceOf classPrototype B
- There are multiple ways of representing these relations, including:
    - A pointsTo B (with linestyle S)
    - A contains B
    - A sharesStyleAttribute S {e.g. thickness} with  B
- By mapping object relations to representations, we can create very versatile diagrams. For example:
    - An execution diagram where (A calls B) == (A contains B) and (B isCalledAfter A) == (A pointsTo B)

We can read the code to determine the objects and relations between them. A user can alter the relation/representation mapping to create diagrams which are useful to them.

## List of object types, currently implemented
- File
- Folder

## List of object relations, currently implemented
- Folder Contains File

## List of relation representations
- A contains B
- A pointsTo B with {linestyle}