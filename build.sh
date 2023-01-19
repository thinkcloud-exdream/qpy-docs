# !/bin/bash

css_dest_dir="out/static/css/theme_default/"
js_dest_dir="out/static/js/theme_default/"
css_src_dir="static/css/theme_default/"
js_src_dir="static/js/theme_default/"
teedoc build
if [ ! -d ${css_src_dir} ]; then
	# mkdir -p ${css_src_dir}
	echo "teedoc 编译失败"
else
cp -R ${css_src_dir}/light.css ${css_dest_dir}/light.css
cp -R ${js_src_dir}/main.js ${js_dest_dir}/main.js
fi

# if [ ! -d ${js_src_dir} ]; then
	# cp
# fi