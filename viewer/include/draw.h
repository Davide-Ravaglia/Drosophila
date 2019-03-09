#define GL_GLEXT_PROTOTYPES
#ifdef _WIN32
#include <windows.h>
#endif
#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <GLUT/glut.h>
#else
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#endif
#include <GL/freeglut.h>
#include <iostream>

#define LIGHT
static constexpr int WIDTH  = 500;
static constexpr int HEIGHT = 500;
float rotate_y = 0.f;
int nframe = 0;

void display();

// ----------------------------------------------------------
// Initialize OpenGL graphic
// ----------------------------------------------------------
void initGL()
{
   glClearColor(0.0f, 0.0f, 0.0f, 1.0f);               // Set background color to black and opaque
   glClearDepth(1.0f);                                 // Set background depth to farthest
   glEnable(GL_DEPTH_TEST);                            // Enable depth testing for z-culling
   glDepthFunc(GL_LEQUAL);                             // Set the type of depth-test
   glShadeModel(GL_SMOOTH);                            // Enable smooth shading
   glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);  // Nice perspective corrections
}

// ----------------------------------------------------------
// Idle OpenGL graphic
// ----------------------------------------------------------
//void idle()
//{
//  // Print OpenGL errors, if there are any (for debugging)
//  if (GLenum err = glGetError())
//    std::cerr << "OpenGL ERROR: " << gluErrorString(err) << std::endl;
//}

// ----------------------------------------------------------
// Keys function callback
// ----------------------------------------------------------
void specialKeys( int key, int x, int y )
{
  switch(key)
  {
    case 102: rotate_y += 5; // GLUT_KEY_RIGHT
    break;
    case 100: rotate_y -= 5; // GLUT_KEY_LEFT
    break;
    case 101: nframe += 1; // GLUT_KEY_UP
    break;
    case 103: nframe -= 1; // GLUT_KEY_DOWN
  }
  glutPostRedisplay();
}

void timer(int extra)
{
  glutPostRedisplay();
  glutTimerFunc(16, timer, 0);
}

// ----------------------------------------------------------
// Start window function (main of OpenGL draw3d)
// ----------------------------------------------------------
void draw_window(int argc, char **argv, const std::string &name_project)
{
  glutInit(&argc, argv);
#if defined(LIGHT)
    glEnable(GL_LIGHT0);                                  // Turn on a light with defaults set
    glEnable(GL_LIGHTING);                                // Turn on lighting
    glEnable(GL_COLOR_MATERIAL);
    glShadeModel(GL_SMOOTH);                          // Allow color
#endif // LIGHT
    glClearColor(0.0, 0.0, 0.0, 1);                         // window background in RGB
    glViewport(0, 0, WIDTH, HEIGHT);                        // Make our viewport the whole window
    glMatrixMode(GL_PROJECTION);                            // Select The Projection Matrix
    glLoadIdentity();                                       // Reset The Projection Matrix
    //gluPerspective(45.0f, WIDTH / HEIGHT, 1, 1.f);
    glMatrixMode(GL_MODELVIEW);                             // Select The Modelview Matrix
    glLoadIdentity();                                       // Reset The Modelview Matrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);     // Clear The Screen And The Depth Buffer
    glLoadIdentity();                                       // Reset The View
    glEnable(GL_DEPTH_TEST);

  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);

  // Create window
  glutInitWindowSize(WIDTH, HEIGHT);
  glutInitWindowPosition(10, 10);
  glutCreateWindow(name_project.c_str());

  glutDisplayFunc(display);
  glutSpecialFunc(specialKeys);
  // Control OpenGL events
  initGL();                       // Our own OpenGL initialization
  glutMainLoop();                 // Enter the infinite event-processing loop
}

