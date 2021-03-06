module.exports = function(grunt) {

  // Project tools config
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),


    // Watch - build dev on changes
    
    watch: {
      files: ['*.html', 'style/*.less', 'js/**.js', 'data/*.json', 'data/*.csv'],
      tasks: ['dev']
    },


    // JS Minification

    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
        preserveComments: 'some'
      },
      build: {
        src: 'tmp/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    },


    // JSHint
    
    jshint: {
      files: ['js/*.js']
    },


    // JS Concatentation

    concat: {
      options: {
        separator: ';'
      },
      dist: {
        src: ['js/*.js', 'js/lib/*.js'],
        dest: 'tmp/<%= pkg.name %>.js'
      }
    },


    // Stylesheet compilation

    less: {
      prod: {
        options: {
          cleancss: true
        },
        files: {
          "build/busing.css": "style/style.less"
        }
      },
      dev: {
        files: {
          "dev/busing.css": "style/style.less"
        }
      }
    },


    // HTML Copying
    
    copy: {
      main: {
        src: ['index.html', 'data/**'],
        dest: 'build/',
      },
      dev: {
        src: ['js/**', 'data/**'],
        dest: 'dev/'
      }
    },


    // ENVironment
    
    env : {
      dev: {
        NODE_ENV: 'DEVELOPMENT',
      },
      build: {
        NODE_ENV: 'PRODUCTION',
      }
    },


    // Preprocessing
    
    preprocess: {
      dev: {
        src: 'index.html',
        dest: 'dev/index.html'
      },
      prod: {
        src: 'index.html',
        dest: 'build/index.html'
      }
    },


    // Directory cleaning
    
    clean: {
      dev: ['dev'],
      prod: ['build', 'tmp']
    }

  });


  // Plugins
  grunt.loadNpmTasks('grunt-env');
  grunt.loadNpmTasks('grunt-preprocess');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-watch');


  // Tasks
  grunt.registerTask('dev', ['clean:dev', 'env:dev', 'preprocess:dev', 'less:dev', 'jshint', 'copy:dev']);
  grunt.registerTask('build', ['clean:prod', 'env:build', 'preprocess:prod', 'less:prod', 'jshint', 'concat', 'uglify']);

};
