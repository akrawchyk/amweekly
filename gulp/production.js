import fs from 'fs'
import gulp from 'gulp'
import cleancss from 'gulp-clean-css'
import uglify from 'gulp-uglify'
import header from 'gulp-header'

const BANNER = fs.readFileSync('banner.txt', 'utf8').replace('@date', (new Date()))


gulp.task('minify:css', () =>
  gulp.src('./amweekly/static/**/*.css')
    .pipe(cleancss())
    .pipe(header(BANNER))
    .pipe(gulp.dest('./amweekly/static/')))

gulp.task('minify:js', () =>
  gulp.src('./amweekly/static/**/*.js')
    .pipe(uglify({
      preserveComments: 'license',
      compressor: {
        screw_ie8: true,
      },
      output: {
        preamble: BANNER,
      },
    }))
    .pipe(gulp.dest('./amweekly/static/')))
