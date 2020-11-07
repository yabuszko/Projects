#include <SFML/Graphics.hpp>
#include <vector>
#include <cmath>
#include <time.h>
#include <sstream>
using namespace sf;
using namespace std;

float tempx;
float tempy;
float newx;
float newy;

float mousex;
int speed = 1;

unsigned iterations = 0;
bool start = false;

class Point {
public:
    Point(float posx, float posy) {
        this->x = posx;
        this->y = posy;

        this->shape.setPosition(this->x, this->y);
        this->shape.setRadius(2);
        this->shape.setFillColor(Color::White);
    }

    void show(RenderWindow* window) const {
        window->draw(this->shape);
    }

    float getx() const {
        return this->x;
    }

    float gety() const {
        return this->y;
    }

private:
    CircleShape shape;
    float x, y;
};

float lerp(float p1, float p2, float len) {
    return p1 + len * (p2 - p1);
}

vector<Point> points;

int main()
{
    RenderWindow window{VideoMode(), "Sierpniski", Style::Fullscreen};
    window.setActive(true);
    window.setFramerateLimit(20);
    window.setMouseCursorGrabbed(true);

    /// SETUP

    Font font;
    if(!font.loadFromFile("arial.ttf")){
        return -1;
    }

    Text text;
    text.setFont(font);
    text.setCharacterSize(23);

    stringstream stext;

    points.push_back(Point(0.f, VideoMode::getDesktopMode().height - 4));
    points.push_back(Point(VideoMode::getDesktopMode().width / 2, 0.f));
    points.push_back(Point(VideoMode::getDesktopMode().width - 4, VideoMode::getDesktopMode().height - 4));

    tempx = points[0].getx();
    tempy = points[0].gety();

    newx = lerp(tempx, points[1].getx(), 0.5);
    newy = lerp(tempy, points[1].gety(), 0.5);

    points.push_back(Point(newx, newy));

    srand(time(NULL));

    Event e;
    while(window.isOpen()) {
        while(window.pollEvent(e)){
            if(e.type == Event::KeyPressed) {
                if(e.key.code == Keyboard::Escape)
                    window.close();
            } else if(e.type == Event::MouseButtonPressed)
                start = !start;
        }

        window.clear();
        stext.str(string()); // clear

        mousex = Mouse::getPosition().x;
        speed = mousex / 80;

        if(start) {
            for(int i = 0; i < speed; i++) {
                iterations++;

                int r = 1 + (rand() % (3 - 1 + 1));
                switch(r) {
                case 1:
                    tempx = points.back().getx();
                    tempy = points.back().gety();

                    newx = lerp(tempx, points[0].getx(), 0.5);
                    newy = lerp(tempy, points[0].gety(), 0.5);
                    points.push_back(Point(newx, newy));
                    break;
                case 2:
                    tempx = points.back().getx();
                    tempy = points.back().gety();

                    newx = lerp(tempx, points[1].getx(), 0.5);
                    newy = lerp(tempy, points[1].gety(), 0.5);
                    points.push_back(Point(newx, newy));
                    break;
                case 3:
                    tempx = points.back().getx();
                    tempy = points.back().gety();

                    newx = lerp(tempx, points[2].getx(), 0.5);
                    newy = lerp(tempy, points[2].gety(), 0.5);
                    points.push_back(Point(newx, newy));
                    break;
                }
            }
        }

        stext << "i: " << iterations;
        text.setString(stext.str());

        for(const auto& p : points)
            p.show(&window);

        window.draw(text);
        window.display();
    }

    return 0;
}
