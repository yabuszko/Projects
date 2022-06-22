#include "Tile.h"

void Tile::load_texture(Texture* txt)
{
	setTexture(txt);
}

void Tile::render_in(RenderTexture* target)
{
	target->draw(*this);
}

Brick::Brick(float x, float y, Texture* texture)
{
	setPosition(x, y);
	setSize(Vector2f(size_x, size_y));
	load_texture(texture);
}
