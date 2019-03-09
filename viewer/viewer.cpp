#include <draw.h>
#include <circles.h>
#include <drosophila.h>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <iterator>
#include <climits>

static constexpr float inf = std::numeric_limits<float>::infinity();
const int num_droso = 10;
static int npts;
std::vector<Drosophila> droso(num_droso);
Circles sphere(.02f, 12, 24);

static constexpr float MIN_W = 1.f;
static constexpr float MAX_W = 2.f; // aka (1.f - (-1.f))

void display()
{
  float x, y;
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Clear color and depth buffers
  glMatrixMode(GL_MODELVIEW);                         // To operate on model-view matrix
                                                      // Clear window and null buffer Z
                                                      // glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                                                      // Reset transformation
  glLoadIdentity();

  nframe = (nframe > npts || nframe < 0) ? 0 : nframe;
  for (int i = 0; i < num_droso; ++i)
  {
    glPushMatrix();
    glRotatef(rotate_y, 0.0, 1.0, 0.0);
    const float x = droso[i].x[nframe];
    const float y = droso[i].y[nframe];
    const float r = rgb_cmap[i * 3    ];
    const float g = rgb_cmap[i * 3 + 1];
    const float b = rgb_cmap[i * 3 + 2];
    sphere.draw( x, y, 0.f, r, g, b );
    glPopMatrix();
  }
  std::cout << "Frame: " << nframe << std::endl;

  //glPushMatrix();
  glFlush();
  glutSwapBuffers();
}


static void usage()
{
  std::cout << "Drosophila viewer usage: ./run filename"             << std::endl
            << std::endl
            << "positional arguments:"                               << std::endl
            << "   filename           Filename with coordinates"     << std::endl
            << std::endl
            << "NOTE: the filename must be formatted as x,y columns" << std::endl
            << "      in particles order"                            << std::endl
            << std::endl
            << "Example:"                                            << std::endl
            << "particle1_x_t1 particle1_y_t1"                       << std::endl
            << "particle1_x_t2 particle1_y_t2"                       << std::endl
            << "particle1_x_t3 particle1_y_t3"                       << std::endl
            << "particle2_x_t1 particle1_y_t1"                       << std::endl
            << "particle2_x_t2 particle1_y_t2"                       << std::endl
            << "particle2_x_t3 particle1_y_t3"                       << std::endl
            << std::endl << std::endl
            << "Usage:"                                              << std::endl
            << "        UP/DOWN    -> frame count"                   << std::endl
            << "        LEFT/RIGHT -> rotate view"                   << std::endl;
}

int main(int argc, char **argv)
{
  if (argc < 2)
  {
    usage();
    std::exit(1);
  }
  std::string filename = argv[1];
  std::ifstream file(filename);
  file.unsetf(std::ios_base::skipws);
  const int nrows = std::count(std::istream_iterator<char>(file),
                               std::istream_iterator<char>(),
                               '\n');
  npts = nrows / num_droso;
  file.clear();
  file.seekg(0, std::ios::beg);
  file.setf(std::ios_base::skipws);

  for (int i = 0; i < num_droso; ++i)
  {
    droso[i].x = new float[npts];
    droso[i].y = new float[npts];
  }

  float x, y;
  float min_x = inf;
  float min_y = inf;
  float max_x = -inf;
  float max_y = -inf;
  for (int i = 0; i < num_droso; ++i)
    for (int j = 0; j < npts; ++j)
    {
      file >> x >> y;
      max_x = (x > max_x) ? x : max_x;
      max_y = (y > max_y) ? y : max_y;
      min_x = (x < min_x) ? x : min_x;
      min_y = (y < min_y) ? y : min_y;
      droso[i].x[j] = x;
      droso[i].y[j] = y;
    }
  file.close();

  // rescale coordinates
  for (int i = 0; i < num_droso; ++i)
    for (int j = 0; j < npts; ++j)
    {
      droso[i].x[j] = ((droso[i].x[j] - min_x) / (max_x - min_x))*MAX_W - MIN_W;
      droso[i].y[j] = ((droso[i].y[j] - min_y) / (max_y - min_y))*MAX_W - MIN_W;
    }

  draw_window(argc, argv, filename);

  return 0;
}

