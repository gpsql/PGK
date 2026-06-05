# Night Thief (PGK Lab15 Project)

## Description
**Night Thief** is a 2D top-down stealth game where you play as a thief trying to steal a precious artifact from a heavily guarded area. Your objective is to navigate the map, avoid the vision cones of patrolling guards, grab the artifact (the yellow square), and reach the exit (the green square).

## Engine and Running Instructions
This project was built using **Python 3** and the **Raylib** library (specifically `raylib-python-cffi`). 

To run the game:
1. Ensure you have Python 3 installed.
2. Install the necessary bindings via pip: `pip install raylib`
3. Run the game from the command line: `python3 main.py`

*Note: The `.wav` audio files were generated using the included `audio_generator.py` script.*

## Custom Mechanic
**Rock Toss Distraction**
By right-clicking anywhere on the screen, the player can throw a "rock". When the rock lands, any guard within hearing distance will abandon their standard patrol route to investigate the sound (Suspicious state). If they find nothing, they will eventually return to their post. This allows the player to manipulate guard positioning to sneak past them.

## Inspiration / Clone Information
This project is heavily inspired by early 2D top-down stealth games, particularly the VR Training missions from **Metal Gear Solid** (PS1).

## Known Bugs and Limitations
- Collision detection with walls uses simple AABB (Axis-Aligned Bounding Box) logic against a circle, which can occasionally result in slightly "sticky" movement if sliding perfectly along a wall corner.
- Guard vision is a simple 360-degree radius check rather than a directional view cone, meaning they will spot you if you get too close even from behind (they have "eyes on the back of their heads"). Vision cannot pass through walls, but this basic line-of-sight check isn't implemented for simplicity.
- Rocks travel to the exact click coordinate linearly; they do not have parabolic physics.
