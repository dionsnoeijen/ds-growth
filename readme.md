# Growth

This is a Blender plugin that simulates branched growth towards particles. This version is still in alpha.

![Example](https://raw.githubusercontent.com/dionsnoeijen/ds-growth/master/growth.gif)

### Things I'm still working on:

- [ ] Make better geometry. (find and fix bugs)
	- [x] The first branches are not connected properly.
	- [x] Probably kill nearly overlapping particles for better results.
	- [X] Fix the straight continuous growing veins. (it should die earlier)
	- [ ] Stacking of vertecies exists, prevent this.
	- [ ] Strange wafers
- [ ] Option to close tips. They will grow towards eachother and close.
- [ ] Option to have branches grow stakes in between for a more rigid structure. (3d printing structures)
- [x] Add a material to the vein clusters.
- [x] Shade smooth.
- [ ] Add thickness patterns.
- [ ] Object origin at cursor.
- [x] Add proper error handling for when wrong items are selected.
- [x] Make option to have the vertex without skin.
- [x] Add choice to add modifiers.
- [x] Add choice to apply or not to apply modifiers.
- [ ] Add settings for subdivision modifier.
- [x] Add info about at with iteration all veins died.
- [ ] Internal limit on iterations to prevent killing the swap size.
- [ ] Add choice if you want to set a material to generated cluster(s)
- [ ] Add input field for material name.
- [ ] Documentation.
