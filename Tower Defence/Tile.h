#pragma once
#include <SFML/Graphics.hpp>
using namespace sf;

class Tile:
    public RectangleShape
{
public:
    Tile(Texture* txt, Vector2f pos, char type, unsigned short id=0);

    char type;
    unsigned short index;
private:
    Texture* texture;
};
