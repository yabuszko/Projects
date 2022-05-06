#include "Tile.h"

Tile::Tile(Texture* txt, Vector2f pos, char type, unsigned short id)
{
	this->texture = txt;
	this->type = type;
	this->index = id;

	setOrigin(0, 0);
	setPosition(pos);
	setTexture(this->texture);
	setSize(static_cast<Vector2f>(this->texture->getSize()));
}
