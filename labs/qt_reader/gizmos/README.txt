Gizmos_v1.1

Instructions:

* Use the mouse to select some objects.
* Use W, E, and R to use translation, rotation and scale gizmos.
* Use middle mouse to continue a transformation even if the mouse is not over the gizmo.
* Use ctrl-click to use the axis' planar mode.

Version History:

v1.1

* Fixed intra module importing
* Moved constants out of __init__.py and into constants.py
* Fixed local transforming for rotation / scale
* Added "complementary" scaling when ctrl-clicking an axis
* Added middle mouse functionality to continue transforming
* Fixed bug where moving the mouse from the rotation gizmo would stop transforming
* Fixed bug where quickly rotating in camera axis would spin the gizmo wildly
* Added support for attaching multiple nodes
* Added marquee selection for demo
* Fixed scale gizmo appearance during transform
* Added concept of default axis
* All transformations now done with matrices
* General code cleanup

v1.0

* Initial release


