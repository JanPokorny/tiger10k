var gulp = require("gulp");
var htmlmin = require('gulp-htmlmin');
var cssmin = require('gulp-cssmin');

gulp.task('default', function() {
	return gulp.src(["./src/*.html"])
		.pipe(htmlmin({
			collapseWhitespace: true,
			conservativeCollapse: true,
			removeComments: true,
			minifyCSS: true
		}))
		.pipe(gulp.dest("./docs"));
});