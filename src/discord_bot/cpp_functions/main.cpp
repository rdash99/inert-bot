//cppimport
#include <pybind11/pybind11.h>

#include <vector>
#include <string>
#include <cmath>
#include <typeinfo>

py::bytes recolor(std::string img, unsigned int height, unsigned int width, unsigned char r, unsigned char g, unsigned char b, float intensity){
	//create vector of prescaled target rgb
	std::vector<unsigned char> rgb = {r, g, b};

	for(size_t i = 0; i<width*height*4; i++){
		if(i%4!=3){
			unsigned char *p = reinterpret_cast<unsigned char*>(&img[i]);
			signed int part = *p + ((signed int) *p * ((float)(rgb[i%4]-*p)/255)*intensity);
			img[i] = part;
		}
	}
	return(img);
}


namespace py = pybind11;

PYBIND11_MODULE(discord_bot, m) {
    m.doc() = R"pbdoc(
        discord_bot cpp module
        -----------------------

        .. currentmodule:: discord_bot

        .. autosummary::
           :toctree: _generate

           recolor

    )pbdoc";

    m.def("add", &recolor, R"pbdoc(
        recolors an image
    )pbdoc");
