#pragma once
#include <SFML/Graphics.hpp>
using namespace sf;
class Tile :
    public RectangleShape
{
public:
    void load_texture(Texture* txt);
    void render_in(RenderTexture* target);
protected:
    int size_x = 64, size_y = 64;
};

class Brick :public Tile {
public:
    Brick(float x, float y, Texture* txt);
};

