import gulp from 'gulp'
import runSequence from 'run-sequence'
import './gulp/build'
import './gulp/production'
import './gulp/utils'
import EXTRAS_GLOB from './gulp/build'


gulp.task('build', (done) => {
  runSequence('clean', ['browserify', 'sass', 'extras'], done)
})

gulp.task('build:production', (done) => {
  runSequence('build', ['minify:css', 'minify:js'], done)
})

gulp.task('watch', ['build', 'watchify'], () => {
  const browserSync = require('browser-sync').create()
  browserSync.init({
    ghostMode: false,
    proxy: `127.0.0.1:${parseInt(process.env.PORT, 10) - 100}`, // subtract 100 because foreman adds 100 to each success worker in the Procfile
    files: './amweekly/static/**/*',
    port: process.env.PORT,
    ui: {
      port: (parseInt(process.env.PORT, 10) + 1)
    }
  })

  // watchify task handles js files
  gulp.watch('./amweekly/static_src/scss/**/*.scss', ['sass'])
  gulp.watch(EXTRAS_GLOB, ['extras'])
})

gulp.task('default', ['build'])
