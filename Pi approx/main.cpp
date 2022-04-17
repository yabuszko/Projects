#include <SFML/Graphics.hpp>
#include <random>
#include <sstream>
#include <iostream>
using namespace sf;
using namespace std;

const unsigned int width = 500, height = 500;

int main() {
	RenderWindow window(VideoMode(width, height), "Pi");
	Event event;

	random_device rd;
	mt19937 mt(rd());
	uniform_int_distribution<int> dist_x(0, width);
	uniform_int_distribution<int> dist_y(0, height);

	Font font;
	if (!font.loadFromFile("Gilroy-Light.otf")) return -1;

	Text text_pi;
	text_pi.setFont(font);
	text_pi.setCharacterSize(32);
	text_pi.setOutlineColor(Color::Black);
	text_pi.setOutlineThickness(3.f);

	stringstream stream_pi;

	CircleShape circle(width / 2);
	circle.setOutlineColor(Color::White);
	circle.setOutlineThickness(1.f);
	circle.setOrigin(width / 2.f, width / 2.f);
	circle.setPosition(width / 2.f, height / 2.f);
	circle.setFillColor(Color(0, 0, 0, 0));

	RenderTexture canvas;
	canvas.create(width, height);
	canvas.clear(Color(50, 50, 50));

	int inside = 0, total = 0;

	while (window.isOpen()) {
		while (window.pollEvent(event)) {
			if (event.type == Event::Closed) {
				window.close();
			}
		}

		window.clear(Color(50, 50, 50));
		stream_pi.str(string());


		for (int i = 0; i < 20; i++) {
			Vector2f new_pos = { static_cast<float>(dist_x(mt)), static_cast<float>(dist_y(mt)) };
			float x = new_pos.x - circle.getPosition().x;
			float y = new_pos.y - circle.getPosition().y;
			if (sqrt(x*x +y*y) < width / 2.f)
			{
				inside++;
				VertexArray temp(Points, 1);
				temp.append(Vertex(new_pos, Color::Yellow));
				canvas.draw(temp);
			}
			else {
				VertexArray temp(Points, 1);
				temp.append(Vertex(new_pos, Color::Green));
				canvas.draw(temp);
			}
			total++;

			canvas.display();
		}

		stream_pi << "PI: " << (double)4 * ((double)inside / (double)total);
		text_pi.setString(stream_pi.str());

		
		Sprite sp(canvas.getTexture());
		window.draw(sp);

		window.draw(circle);
		window.draw(text_pi);

		window.display();
	}

	return 0;
}