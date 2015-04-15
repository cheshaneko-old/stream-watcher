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
            },
            bower: {
                cwd: '',
                src: [ 'bower_components/**/*', 'bower.json' ],
                dest: 'build',
                expand: true
            }
        },
        clean: {
            build: {
                src: [ 'build' ]
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
        },
        bowerInstall: {
            build: {
                // Point to the files that should be updated when 
                // you run `grunt bower-install` 
                src: [
                    'build/*.html'   // .html support... 
                ],

                // Optional: 
                // --------- 
                cwd: 'build',
                dependencies: true,
                devDependencies: false,
                exclude: [],
                fileTypes: {},
                ignorePath: '',
                overrides: {}
            }
        } 
    
        
    });


    // Task definition
    grunt.registerTask('default', []);
    grunt.registerTask('build', ['clean:build', 'copy:build', 'copy:bower', 'bowerInstall:build', 'includeSource:build']);
};
