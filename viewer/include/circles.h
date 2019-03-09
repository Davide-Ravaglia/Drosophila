#ifndef CIRCLES_H
#define CIRCLES_H
#ifdef _WIN32
#include <windows.h>
#endif
#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif
#include <memory>
#include <cmath>
#include <array>
static constexpr float m_pi   = 3.141519f;
static constexpr float m_pi_2 = 1.570759f;
static constexpr float m_pi2  = m_pi * 2.f;

static constexpr int num_colors_cmap = 19;
static constexpr std::array<float, 19 * 3> rgb_cmap {
                                                      0.078431f, 0.078431f, 0.078431f,
                                                      0.266667f, 0.133333f, 0.600000f,
                                                      0.231373f, 0.047059f, 0.741176f,
                                                      0.200000f, 0.066667f, 0.733333f,
                                                      0.266667f, 0.266667f, 0.866667f,
                                                      0.066667f, 0.666667f, 0.733333f,
                                                      0.070588f, 0.741176f, 0.725490f,
                                                      0.133333f, 0.800000f, 0.666667f,
                                                      0.411765f, 0.815686f, 0.145098f,
                                                      0.666667f, 0.800000f, 0.133333f,
                                                      0.815686f, 0.764706f, 0.062745f,
                                                      0.800000f, 0.733333f, 0.200000f,
                                                      0.996078f, 0.682353f, 0.176471f,
                                                      1.000000f, 0.600000f, 0.200000f,
                                                      1.000000f, 0.400000f, 0.266667f,
                                                      1.000000f, 0.266667f, 0.133333f,
                                                      1.000000f, 0.200000f, 0.066667f,
                                                      0.933333f, 0.066667f, 0.000000f,
                                                      0.972549f, 0.047059f, 0.070588f
                                                    };

class Circles
{
protected:
  int nindices;
  std::unique_ptr<GLfloat[]> vertices, normals, texcoords;
  std::unique_ptr<GLushort[]> indices;

public:
  Circles() {};
  Circles(const float &radius, const int &rings, const int &sectors);
  void draw(const GLfloat &x, const GLfloat &y, const GLfloat &z, const GLfloat &R, const GLfloat &G, const GLfloat &B );
};


#endif // CIRCLES_H
