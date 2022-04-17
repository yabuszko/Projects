#include <SFML/Graphics.hpp>
#include <cmath>
#include <sstream>
#include <vector>

#include "settings.h"
using namespace std;
using namespace sf;

class Ball :public CircleShape {
public:
	Ball(float r, Color col, Vector2f pos, float m=0.f) {
		setRadius(r);
		setOrigin(r, r); // centre

		this->mass = m;

		this->position = pos;
		setPosition(pos);
		setFillColor(col);
	}

	void show(RenderWindow* target) const {
		target->draw(*this);
	}

	void onHold(Vector2f pos, bool p) {
		if (getGlobalBounds().contains(lastpos)) { // mouse over
			if (p) {
				this->position = static_cast<Vector2f>(Mouse::getPosition());
				setPosition(this->position);

				set_new_values = true;
			}
			else
				set_new_values = false;
		}

		lastpos = static_cast<Vector2f>(Mouse::getPosition());
	}

private:
	Vector2f position;
	Vector2f lastpos = static_cast<Vector2f>(Mouse::getPosition());

public:
	float mass;
};

class Line :public RectangleShape {
public:
	Line(Vector2f pos, float width, float angle, float len) {
		this->thickness = width;
		this->position = pos;
		this->rotation = angle;

		this->velocity = 0;
		this->acceleration = 0;

		this->length = len;

		setPosition(this->position);
		setSize(Vector2f(this->thickness, this->length));
		setFillColor(Color(50, 50, 50));

		setRotation(this->rotation * 180 / pi);
		//setOrigin(getSize().x / 2, 0.f);
	}

	void update() {
		this->velocity += this->acceleration;

		if (to_rest)
			this->acceleration *= 0.999;

		float new_angle = getRotation() * pi / 180 + this->velocity;

		setRotation(new_angle * 180/pi);
	}

	void show(RenderWindow* target) const {
		target->draw(*this);
	}
public:
	float length;

private:
	float thickness;
	float rotation;
	Vector2f position;

public:
	float velocity;
	float acceleration;
};

class Trace {
public:
	Trace(RenderTexture* target) 
	:position_init({0,0}), position_final({0,0})
	{
		this->body = target;
		this->body->clear();
	}

	void get_data(Vector2f pos) {
		this->position_init = pos;
	}

	void leave_dot(Vector2f pos, Color col) {
		this->point_a.position = position_init;
		this->point_a.color = col;
		
		this->point_b.position = pos;
		this->point_b.color = col;

		this->position_init = pos;

		VertexArray temp_arr(LinesStrip, 2);
		temp_arr[0] = this->point_a;
		temp_arr[1] = this->point_b;
		this->body->draw(temp_arr);
	}
private:
	Vertex point_a;
	Vertex point_b;

	RenderTexture* body;

	Vector2f position_init;
	Vector2f position_final;
};

int main() {
	read_data();

	ContextSettings settings;
	settings.antialiasingLevel = 8;

	RenderWindow window(VideoMode(0, 0), "Double pendulum", Style::Fullscreen, settings);
	window.setFramerateLimit(60);
	window.setKeyRepeatEnabled(false);

	// Pivot
	Ball pivot(10.f, Color::White, Vector2f(VideoMode::getDesktopMode().width / 2, VideoMode::getDesktopMode().height / 2));
	
	// RenderTexture
	RenderTexture canvas;
	canvas.create(VideoMode::getDesktopMode().width, VideoMode::getDesktopMode().height);

	// coords translation
	Vector2f translated = pivot.getPosition();

	// Other objects
	Line line1(pivot.getPosition(), 1.f, -pi/2, len1);

	unsigned int faster = 0;
	bool freetransform = false;
	bool pressed = false;

	Ball m1(ma1 / 2, Color(45, 129, 224, 100), Vector2f(translated.x + line1.length * sin(-line1.getRotation() * pi / 180),
		translated.y + line1.length * cos(line1.getRotation() * pi / 180)), ma1);

	Line line2(m1.getPosition(), 1.f, -pi/2, len2);

	Ball m2(ma2 / 2, Color(0, 255, 0, 100), Vector2f(m1.getPosition().x + line2.length * sin(-line2.getRotation() * pi / 180),
		m1.getPosition().y + line2.length * cos(line2.getRotation() * pi / 180)), ma2);

	// Fonts
	Font font;
	if(!font.loadFromFile("Gilroy-Light.otf")) return -1;

	Text text1, text2, text3, text4, text5, text6;
	text1.setFont(font);
	text1.setCharacterSize(20);
	text1.setPosition(0, 0);

	text2.setFont(font);
	text2.setCharacterSize(20);
	text2.setFillColor(Color(45, 129, 224, 100));
	text2.setPosition(0, 25);

	text3.setFont(font);
	text3.setCharacterSize(20);
	text3.setFillColor(Color(0, 255, 0, 100));
	text3.setPosition(0, 50);

	text4.setFont(font);
	text4.setCharacterSize(20);
	text4.setFillColor(Color(45, 129, 224, 100));
	text4.setPosition(0, 75);

	text5.setFont(font);
	text5.setCharacterSize(20);
	text5.setFillColor(Color(0, 255, 0, 100));
	text5.setPosition(0, 100);

	text6.setFont(font);
	text6.setCharacterSize(10);
	text6.setPosition(0, VideoMode::getDesktopMode().height - 10);

	stringstream stext1, stext2, stext3, stext4, stext5;


	// Trace
	Trace trace_1(&canvas);
	Trace trace_2(&canvas);
	trace_1.get_data(m1.getPosition());
	trace_2.get_data(m2.getPosition());

	while (window.isOpen()) {
		Event e;
		while (window.pollEvent(e)) {
			if (e.type == Event::KeyPressed) {
				if (e.key.code == Keyboard::Escape)
					window.close();
				else if (e.key.code == Keyboard::Space) {
					if (faster == 0) faster = 1;
					else faster = 0;
				}
				else if (e.key.code == Keyboard::T) {
					freetransform = !freetransform;
				}
				else if (e.key.code == Keyboard::Q) {
					if(freetransform)
					if (m1.mass >= 10) {
						m1.mass -= 5;
						m1.setRadius(m1.getRadius() - 2.5);
						m1.setOrigin(m1.getRadius(), m1.getRadius());
					}
				}
				else if (e.key.code == Keyboard::W) {
					if (freetransform) {
						if (m1.mass <= 100) {
							m1.mass += 5;
							m1.setRadius(m1.getRadius() + 2.5);
							m1.setOrigin(m1.getRadius(), m1.getRadius());
						}
					}
				}
				else if (e.key.code == Keyboard::A) {
					if (freetransform)
					if (m2.mass >= 10) {
						m2.mass -= 5;
						m2.setRadius(m2.getRadius() - 2.5);
						m2.setOrigin(m2.getRadius(), m2.getRadius());
					}
				}
				else if (e.key.code == Keyboard::S) {
					if (freetransform)
					if (m2.mass <= 100) {
						m2.mass += 5;
						m2.setRadius(m2.getRadius() + 2.5);
						m2.setOrigin(m2.getRadius(), m2.getRadius());
					}
				}
				else if (e.key.code == Keyboard::C) {
					canvas.clear(Color::Black);
					trace_1.get_data(m1.getPosition());
					trace_2.get_data(m2.getPosition());
				}
			}
			else if (e.type == Event::MouseButtonPressed) {
				pressed = true;
			}
			else if (e.type == Event::MouseButtonReleased) {
				pressed = false;
			}
		}

		// update
		stext1.str(string()); stext2.str(string()); stext3.str(string()); stext4.str(string()); stext5.str(string());

		if (!freetransform) {
			for (size_t i = 0; i < 1 + speed_factor * faster; i++) {
				float num1 = -gravitational_acceleration * (2 * m1.mass + m2.mass) * sin(line1.getRotation() * pi / 180);
				float num2 = -m2.mass * gravitational_acceleration * sin((line1.getRotation() - 2 * line2.getRotation()) * pi / 180);
				float num3 = -2 * sin((line1.getRotation() - line2.getRotation()) * pi / 180);
				float num4 = line2.velocity * line2.velocity * line2.length + line1.velocity * line1.velocity * line1.length *
					cos((line1.getRotation() - line2.getRotation()) * pi / 180);
				float den = line1.length * 2 * (m1.mass + m2.mass - m2.mass * cos((2 * line1.getRotation() - 2 * line2.getRotation()) * pi / 180));
				line1.acceleration = (num1 + num2 + num3 * num4) / den;

				num1 = 2 * sin((line1.getRotation() - line2.getRotation()) * pi / 180);
				num2 = line1.velocity * line1.velocity * line1.length * (m1.mass + m2.mass);
				num3 = gravitational_acceleration * (m1.mass + m2.mass) * cos(line1.getRotation() * pi / 180);
				num4 = line2.velocity * line2.velocity * line2.length * m2.mass * cos((line1.getRotation() - line2.getRotation()) * pi / 180);
				den = line2.length * 2 * (m1.mass + m2.mass - m2.mass * cos((2 * line1.getRotation() - 2 * line2.getRotation()) * pi / 180));
				line2.acceleration = num1 * (num2 + num3 + num4) / den;

				line1.update();
				line2.update();

				m1.setPosition(Vector2f(translated.x + line1.length * sin(-line1.getRotation() * pi / 180),
					translated.y + line1.length * cos(line1.getRotation() * pi / 180)));
				m2.setPosition(Vector2f(m1.getPosition().x + line2.length * sin(-line2.getRotation() * pi / 180),
					m1.getPosition().y + line2.length * cos(line2.getRotation() * pi / 180)));
				line2.setPosition(m1.getPosition());

				trace_1.leave_dot(m1.getPosition(), Color(30, 103, 186));
				trace_2.leave_dot(m2.getPosition(), Color(72, 217, 109));
				canvas.display();
			}
		}
		else{
			m1.onHold(static_cast<Vector2f>(Mouse::getPosition()), pressed);
			m2.onHold(static_cast<Vector2f>(Mouse::getPosition()), pressed);

			if (set_new_values) {
				line1.length = sqrt(pow(m1.getPosition().y - pivot.getPosition().y, 2) + pow(m1.getPosition().x - pivot.getPosition().x, 2));
				line1.setSize(Vector2f(line1.getSize().x, line1.length));
				len1 = line1.length;

				float angle1 = asin((m1.getPosition().x - pivot.getPosition().x) / len1);
				if (m1.getPosition().y >= line1.getPosition().y)
					line1.setRotation(-angle1 * 180 / pi);
				else { // arcsin(x) = <-pi/2, pi/2>
					line1.setRotation(180 + angle1 * 180 / pi); // pi/2
				}

				line2.setPosition(m1.getPosition());
				line2.length = sqrt(pow(m2.getPosition().y - m1.getPosition().y, 2) + pow(m2.getPosition().x - m1.getPosition().x, 2));
				line2.setSize(Vector2f(line2.getSize().x, line2.length));
				len2 = line2.length;

				float angle2 = asin((m2.getPosition().x - m1.getPosition().x) / len2);
				if (m2.getPosition().y >= line2.getPosition().y)
					line2.setRotation(-angle2 * 180 / pi);
				else { // arcsin(x) = <-pi/2, pi/2>
					line2.setRotation(180 + angle2 * 180 / pi); // pi/2
				}

				canvas.clear(Color::Black);
				trace_1.get_data(m1.getPosition());
				trace_2.get_data(m2.getPosition());
			}
		}

		stext1 << "g: 0.1 m/s^2";
		stext2 << "T -> (Q/W) m1: " << m1.mass << " kg";
		stext3 << "T -> (A/S) m2: " << m2.mass << " kg";
		stext4 << "r1: " << trunc(line1.length);
		stext5 << "r2: " << trunc(line2.length);

		text1.setString(stext1.str());
		text2.setString(stext2.str());
		text3.setString(stext3.str());
		text4.setString(stext4.str());
		text5.setString(stext5.str());
		text6.setString("by Oliwier Moskalewicz 2022");

		// draw
		window.clear(Color::Black);
		Sprite container;
		container.setTexture(canvas.getTexture());
		container.setPosition(0, 0);

		window.draw(container);

		line1.show(&window);
		line2.show(&window);

		pivot.show(&window);
		m1.show(&window);
		m2.show(&window);

		window.draw(text1);
		window.draw(text2);
		window.draw(text3);
		window.draw(text4);
		window.draw(text5);
		window.draw(text6);

		window.display();
		
	}

	return 0;
}