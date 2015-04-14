//Gruntfile
module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);

    //Initializing the configuration object
    grunt.initConfig({
        copy: {
            build: {
                cwd: 'app',
                src: [ '**' ],
                dest: 'build',
                expand: true
            }
        },
        clean: {
            build: {
                src: [ 'build' ]
            }
        },
        bower: {
            build: {
                dest: 'build/bower/',
                js_dest: 'build/scripts/',
                css_dest: 'build/styles/'
            }
        },
        includeSource: {
            options: {
                // Task-specific options go here.
                basePath: 'build'
            },
            build: {
                // Target-specific file lists and/or options go here.
                files: {
                    'build/index.html': 'build/index.html'
                }
            }
        }
    
        
    });


    // Task definition
    grunt.registerTask('default', []);
    grunt.registerTask('build', ['clean:build', 'copy:build', 'bower:build', 'includeSource:build']);
};
