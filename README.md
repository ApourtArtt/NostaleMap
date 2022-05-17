# NostaleMap

Map viewer for Nostale, using Blender.

## How it works
### Short answer : it does not
### Long answer :
It requires multiple things :
- Blender
- A tool to unpack Nostale files ([https://github.com/Pumba98/OnexExplorer](OnexExplorer) for example)
- Game files
- Brain
- Eyes
- Hands
- I probably forgot something


#### Preparation

You will need to unpack NStuData which is the archive storing map structure (the fog, the constraint like "can the map be rotate" (imagine miniland vs nosville), which objects are on it, where they are, etc.) \
You will also need to unpack NStgData which stores the 3D .obj and .mtl (not sure for the second, I can't remember and I am too lazy to check)
And finally, you will need to unpack NStpData which stores the images used by the .mtl files

Then you will need to create a folder, wherever you want and call it "maps", inside of it, a folder named "3dmodels".
> |_ maps \
> | |_ 3dmodels

In 3dmodels you will save all the object related files (.obj, .jpg, .png if there is any, .mtl, ...) \
In maps, you will save the map structures, coming from NStuData. It should be in .map extension - AFAIR Onex saves in .bin, you can change the extension easily with the following command: `ren *.bin *.map`

##### Display the map

- Start Blender
- Go to the "Scripting" tab - google if it is not shown
- Click on the "New" button
- Paste blender-script.py code into the textbox
- Click on the "Run script" button
In the bottom left panel, a new group has appeared: "Nostale Map Manager", deploy it
- Click on the "Import Map file" button
- Go into the "maps" and select "63.map"

Now the map should be displayed on the 3D viewer.

## How to improve
So far, there are multiple known issues :
1) Rotations are completely ignored
2) Objects with "Intertype" of 1 are shown - they should be ignored (I will come back to that later)
3) Objects are not always where they need to be (same)

Maybe some interesting information will be posted there: https://www.elitepvpers.com/forum/nostale/5027015-how-manage-nostale-map.html#post39189702
