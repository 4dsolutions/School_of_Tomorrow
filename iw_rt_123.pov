
// Persistence of Vision Ray Tracer Scene Description File
// File: xyz.pov
// Vers: 3.6
// Desc: test file
// Date: Sat Sep  7 09:49:33 2019
// Auth: me
// ==== Standard POV-Ray Includes ====
#include "colors.inc"     // Standard Color definitions
// include "textures.inc"   // Standard Texture definitions
// include "functions.inc"  // internal functions usable in user defined functions

// ==== Additional Includes ====
// Don't have all of the following included at once, it'll cost memory and time
// to parse!
// --- general include files ---
// include "chars.inc"      // A complete library of character objects, by Ken Maeno
// include "skies.inc"      // Ready defined sky spheres
// include "stars.inc"      // Some star fields
// include "strings.inc"    // macros for generating and manipulating text strings

// --- textures ---
// include "finish.inc"     // Some basic finishes
// include "glass.inc"      // Glass textures/interiors
// include "golds.inc"      // Gold textures
// include "metals.inc"     // Metallic pigments, finishes, and textures
#include "stones.inc"     // Binding include-file for STONES1 and STONES2
// include "stones1.inc"    // Great stone-textures created by Mike Miller
// include "stones2.inc"    // More, done by Dan Farmer and Paul Novak
// include "woodmaps.inc"   // Basic wooden colormaps
// include "woods.inc"      // Great wooden textures created by Dan Farmer and Paul Novak

global_settings {assumed_gamma 1.0}
global_settings {ambient_light rgb<1, 1, 1> }

// perspective (default) camera
camera {
  location  <6, 0.1, 0.2>
  rotate    <35, 35, 10.0>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}

// create a regular point light source
light_source {
  0*x                  // light's position (translated below)
  color rgb <1,1,1>    // light's color
  translate <-20, 15, 10>
}

// create a regular point light source
light_source {
  0*x                  // light's position (translated below)
  color rgb <1,1,1>    // light's color
  translate <20, -15, -10>
}

background { color rgb <1.0, 1.0, 1.0> }
sphere { < 0, 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < -0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0, -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0, 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < -0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0, -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < 0, -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < -0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < 0, -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < 0, 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, < -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, < 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, < 0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, < -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < 0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, < -0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < -0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, < 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, < -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0, -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, < 0, -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < -0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < 0, -0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 0, 0.618033988749895*sqrt(2) >, < 0, -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), -0.381966011250105*sqrt(2), 0 >, < 0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 0, -0.618033988749895*sqrt(2) >, < -0.618033988749895*sqrt(2), 0.381966011250105*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0, 1, 1> } } no_shadow }
sphere { < 0, 0, 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <1, 0, 0> } } no_shadow }
sphere { < 0, 1.0*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <1, 0, 0> } } no_shadow }
sphere { < 1.0*sqrt(2), 0, 0 >, 0.03 texture { pigment { color rgb <1, 0, 0> } } no_shadow }
sphere { < -1.0*sqrt(2), 0, 0 >, 0.03 texture { pigment { color rgb <1, 0, 0> } } no_shadow }
sphere { < 0, -1.0*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <1, 0, 0> } } no_shadow }
sphere { < 0, 0, -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 0, 1.0*sqrt(2) >, < 1.0*sqrt(2), 0, 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), 0, 0 >, < 0, 0, -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 1.0*sqrt(2), 0 >, < 0, 0, -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 1.0*sqrt(2), 0 >, < -1.0*sqrt(2), 0, 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), 0, 0 >, < 0, -1.0*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 1.0*sqrt(2), 0 >, < 1.0*sqrt(2), 0, 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), 0, 0 >, < 0, -1.0*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, -1.0*sqrt(2), 0 >, < 0, 0, -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 0, 1.0*sqrt(2) >, < 0, 1.0*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), 0, 0 >, < 0, 0, -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 0, 1.0*sqrt(2) >, < -1.0*sqrt(2), 0, 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
cylinder { < 0, 0, 1.0*sqrt(2) >, < 0, -1.0*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <1, 0, 0> } } no_shadow }
sphere { < 1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < -1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < -1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < 1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < -1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < 1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < 1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < -1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, < -1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, < -1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, < -1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, < 1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, < 1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, < 1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, < -1.0*sqrt(2), -1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, < -1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, < 1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, < 1.0*sqrt(2), -1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < -1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, < -1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
cylinder { < 1.0*sqrt(2), 1.0*sqrt(2), 1.0*sqrt(2) >, < 1.0*sqrt(2), 1.0*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0, 1, 0> } } no_shadow }
sphere { < -0.381966011250105*sqrt(2), 1.0*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.381966011250105*sqrt(2), 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 1.0*sqrt(2), 0, -0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0, -0.381966011250105*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -1.0*sqrt(2), -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.381966011250105*sqrt(2), -1.0*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.381966011250105*sqrt(2), -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), 0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.618033988749895*sqrt(2), 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 5.55111512312578e-17*sqrt(2), -1.0*sqrt(2), 0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0.618033988749895*sqrt(2), 0, -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), -1.0*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 0, -1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -1.0*sqrt(2), 0.618033988749895*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < -1.0*sqrt(2), -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 1.0*sqrt(2), -0.618033988749895*sqrt(2), 0 >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
sphere { < 1.0*sqrt(2), 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture { pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < -1.0*sqrt(2), 0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2) >, < -1.0*sqrt(2), -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, < 0, -1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, < 1.0*sqrt(2), 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < -1.0*sqrt(2), -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, < 1.0*sqrt(2), 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), -0.618033988749895*sqrt(2) >, < -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), -1.0*sqrt(2) >, < -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -1.0*sqrt(2), -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, < -1.0*sqrt(2), -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), -1.0*sqrt(2) >, < -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749895*sqrt(2), 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, < -1.0*sqrt(2), -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < 1.0*sqrt(2), -0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, < 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), -1.0*sqrt(2), 0 >, < 1.0*sqrt(2), -0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < 0, -1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < -0.618033988749895*sqrt(2), 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0, -0.381966011250105*sqrt(2), -1.0*sqrt(2) >, < 0, -1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.381966011250105*sqrt(2), -1.0*sqrt(2), 0 >, < 0, -1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), -1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < 0.381966011250105*sqrt(2), -1.0*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < 1.0*sqrt(2), 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), 1.0*sqrt(2) >, < -0.618033988749895*sqrt(2), 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < 0.381966011250105*sqrt(2), 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, < -5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), 0, -1.0*sqrt(2) >, < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < 0.618033988749895*sqrt(2), 0, -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), 0, -1.0*sqrt(2) >, < 0, -0.381966011250105*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < 1.0*sqrt(2), 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < 0, -1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), -1.0*sqrt(2) >, < 0.618033988749895*sqrt(2), 0, -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, < 1.0*sqrt(2), -0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < 5.55111512312578e-17*sqrt(2), -1.0*sqrt(2), 0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 1.0*sqrt(2), 0, -0.381966011250105*sqrt(2) >, < 1.0*sqrt(2), 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2) >, < -1.0*sqrt(2), 0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2), 1.0*sqrt(2) >, < 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2), 1.0*sqrt(2) >, < -0.618033988749895*sqrt(2), 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < -1.0*sqrt(2), 0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), -0.618033988749895*sqrt(2) >, < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, < -1.0*sqrt(2), -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < 5.55111512312578e-17*sqrt(2), -1.0*sqrt(2), 0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -1.0*sqrt(2), -5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, < -1.0*sqrt(2), 0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < 1.0*sqrt(2), -0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), -1.0*sqrt(2) >, < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0, -0.381966011250105*sqrt(2), -1.0*sqrt(2) >, < -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), -1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 1.0*sqrt(2), 0 >, < 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), -0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < -0.381966011250105*sqrt(2), 1.0*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, < 1.0*sqrt(2), 5.55111512312578e-17*sqrt(2), 0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, < 0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), -1.0*sqrt(2), 0.618033988749895*sqrt(2) >, < -0.381966011250105*sqrt(2), -1.0*sqrt(2), 5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -5.55111512312578e-17*sqrt(2), -0.381966011250105*sqrt(2), 1.0*sqrt(2) >, < 5.55111512312578e-17*sqrt(2), -1.0*sqrt(2), 0.618033988749895*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 1.0*sqrt(2), 0, -0.381966011250105*sqrt(2) >, < 1.0*sqrt(2), -0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2), -0.618033988749895*sqrt(2) >, < -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749895*sqrt(2), 5.55111512312578e-17*sqrt(2), 1.0*sqrt(2) >, < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), 0.618033988749894*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.381966011250105*sqrt(2), 1.0*sqrt(2), 0 >, < -1.0*sqrt(2), 0.618033988749895*sqrt(2), 0 >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < 0.618033988749895*sqrt(2), 0, -1.0*sqrt(2) >, < 1.0*sqrt(2), 0, -0.381966011250105*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
cylinder { < -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2), -0.618033988749894*sqrt(2) >, < -1.0*sqrt(2), -0.618033988749895*sqrt(2), -5.55111512312578e-17*sqrt(2) >, 0.03 texture {pigment { color rgb <0.4117647058823529, 0.20784313725490197, 0.611764705882353> } } no_shadow }
