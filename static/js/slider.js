/*!
 * jQuery lightweight plugin boilerplate
 * Original author: @sahanhaz
 * Further changes, comments: @sahanhaz
 * Licensed under the MIT license
 */

// the semi-colon before the function invocation is a safety
// net against concatenated scripts and/or other plugins
// that are not closed properly.
;(function ( $, window, document, undefined ) {

    // undefined is used here as the undefined global
    // variable in ECMAScript 3 and is mutable (i.e. it can
    // be changed by someone else). undefined isn't really
    // being passed in so we can ensure that its value is
    // truly undefined. In ES5, undefined can no longer be
    // modified.

    // window and document are passed through as local
    // variables rather than as globals, because this (slightly)
    // quickens the resolution process and can be more
    // efficiently minified (especially when both are
    // regularly referenced in your plugin).

    // Create the defaults once
    var pluginName = "slider",
        defaults = {
            startValue: 200,
            offset : 200,
            menuDelay : 400,
            menuColor : ['red','green']
        };

    // The actual plugin constructor
    function Plugin( element, options ) {
        this.element = element;

        // jQuery has an extend method that merges the
        // contents of two or more objects, storing the
        // result in the first object. The first object
        // is generally empty because we don't want to alter
        // the default options for future instances of the plugin
        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;

        this.init();
    }

    Plugin.prototype = {

        init: function() {
            // Place initialization logic here
            // You already have access to the DOM element and
            // the options via the instance, e.g. this.element
            // and this.options
            // you can add more functions like the one below and
            // call them like so: this.yourOtherFunction(this.element, this.options).

            var $block = this;
            var index = 0;
            var lastIndex = 0;

            $(this.element).find('.link a').on('mouseover' , function () {
                index = $(this).parent().parent().index();
                if(index == 0) {
                    $('.list-item').removeClass('bg1 bg2').addClass('bg0');
                    if(lastIndex > index) {
                        Plugin.prototype.calcPosition(3 , $block.options.startValue);
                    }
                    else {
                        Plugin.prototype.calcPosition(0 , $block.options.startValue + $block.options.offset);
                    }
                    Plugin.prototype.showMenu($(this) , $block.options.menuDelay , $block.options.menuColor , index);
                }
                else if(index == 1) {
                    $('.list-item').removeClass('bg0 bg2').addClass('bg1');
                    if(lastIndex > index) {
                        Plugin.prototype.calcPosition(3 , $block.options.startValue);
                    }
                    else {
                        Plugin.prototype.calcPosition(0 , $block.options.startValue + $block.options.offset);
                    }
                    Plugin.prototype.showMenu($(this) , $block.options.menuDelay , $block.options.menuColor , index);
                }
                else {
                    $('.list-item').removeClass('bg0 bg1').addClass('bg2');
                    if(lastIndex > index) {
                        Plugin.prototype.calcPosition(3 , $block.options.startValue);
                    }
                    else {
                        Plugin.prototype.calcPosition(0 , $block.options.startValue + $block.options.offset);
                    }
                    Plugin.prototype.showMenu($(this) , $block.options.menuDelay , $block.options.menuColor , index);
                }
                lastIndex = index;
            });
            $(this.element).find('.link').on('mouseleave' , function () {
                Plugin.prototype.hideMenu();
            });
            this.calcPosition(0 , $block.options.startValue);
        },
        calcPosition: function(inc , delay) {
            var $block = $('.nav-container');
            $block.find('.list-item').css('background-position-x','0');
            $block.find('.list-item').each(function() {
                var index = $(this).index();
                var incrimentalVal = inc - index;
                var left = 265 * incrimentalVal ;
                $(this).stop().animate( {backgroundPositionX: left} ,delay);
            });
        },
        showMenu: function(element , menuDelay , menuColor , index) {
            var $block = $('.nav-container');
            var element = element.parent().parent();
            $block.find('.menu-wrapper .menu-block').removeClass('active');
            var activeLeft = element.position().left;
            var activeHeight = $(element).find('.menu').outerHeight();
            $block.find('.menu-wrapper .moving-block').show();
            $block.find('.menu-wrapper .moving-block').stop().animate( {left: activeLeft , height: activeHeight} ,menuDelay+100);
            $block.find('.menu-wrapper .moving-block').css('background-color' , menuColor[index]);
            setTimeout(function(){ element.addClass('active'); }, menuDelay);
        },
        hideMenu: function() {
            var $block = $('.nav-container');
            $block.find('.menu-wrapper .menu-block').removeClass('active');
            $block.find('.menu-wrapper .moving-block').hide();
        }
    };

    // A really lightweight plugin wrapper around the constructor,
    // preventing against multiple instantiations
    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName,
                new Plugin( this, options ));
            }
        });
    };

})( jQuery, window, document );
