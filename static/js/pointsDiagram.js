//variables for SVG viewport
var canvWidth = 330;
var canvHeight = 260;
var margin = 50;

//create SVG viewport
var svgElement = d3.select('#chart')
    .append('svg:svg').attr({
    'width': canvWidth,
    'height': canvHeight
}).style('border','0px solid');

//label data
var labelData = [
    {'cx': 120, 'cy': 305, 'label': 'Kapitel behandelt'},
    {'cx': 120, 'cy': 335, 'label': 'Punkte erhalten'},
    {'cx': 120, 'cy': 365, 'label': 'Punkte abgegeben'},
    {'cx': 160, 'cy': 161, 'label': '4'},
    {'cx': 199, 'cy': 140, 'label': '3'},
    {'cx': 232, 'cy': 121, 'label': '2'},
    {'cx': 263, 'cy': 102, 'label': '1'}
];

//path node data for outlines
var pathOutlineData = [
    {'x': 165, 'y': 158}, {'x': 145, 'y': 170}, {'x': 145, 'y': 193}, //3
    {'x': 165, 'y': 204}, {'x': 185, 'y': 192}, {'x': 185, 'y': 169}, //6
    {'x': 165, 'y': 158}, {'x': 145, 'y': 170}, {'x': 145, 'y': 30 }, //9
    {'x': 165, 'y': 42 }, {'x': 185, 'y': 30 }, {'x': 185, 'y': 169}, //12
    {'x': 306, 'y': 239}, {'x': 286, 'y': 251}, {'x': 286, 'y': 274}, //15
    {'x': 165, 'y': 204}, {'x': 45 , 'y': 274}, {'x': 45 , 'y': 251}, //18
    {'x': 25 , 'y': 239}, {'x': 145, 'y': 170}
];

//path node data for positive grade scale outlines
var pathPosOutlineData = [
    {'x': 185, 'y': 147}, {'x': 267, 'y': 99 }, {'x': 287, 'y': 111},
    {'x': 287, 'y': 134}, {'x': 205, 'y': 181}
];

//path node data for grade 3 seperator
var pathGradeSeperator3 = [
    {'x': 202, 'y': 137}, {'x': 221, 'y': 149}, {'x': 221, 'y': 172}
]

//path node data for grade 2 seperator
var pathGradeSeperator2 = [
    {'x': 232, 'y': 120}, {'x': 252, 'y': 131}, {'x': 252, 'y': 154}
]

//gradient vars
var minYg = 0;
var maxYg = 200;

//gradient definition
var gradient = svgElement
    .append('linearGradient')
    .attr('y1', minYg)
    .attr('y2', maxYg)
    .attr('x1', '0')
    .attr('x2', '0')
    .attr('id', 'gradient')
    .attr('gradientUnits', 'userSpaceOnUse')

//gradient start color
gradient
    .append('stop')
    .attr('offset', '0')
    .attr('stop-color', '#b7ffb7')

//gradient end color
gradient
    .append('stop')
    .attr('offset', '0.8')
    .attr('stop-color', '#53c03e')

//draw bar for evaluated points
var draw_all_chapter_badge = function(b) {

    //bar limit
    if (b.progress >= b.maximum) {
        b.progress = b.maximum
    }

    //setting height of bar according to progress
    height = 140 * (b.progress / b.maximum)

    var bar1ConstructorValues = [
        //bar 1 outlines
        //{'x': 0, 'y': 0, 'widt': 20, 'heig': 140, 'skY': 30, 'fill': 'blue'},
        //{'x': 20, 'y': 22.91025543212891, 'widt': 20, 'heig': 140, 'skY': -30, 'fill': 'blue'},
        //bar 1  height rausgeschrieben
        {'x': 0, 'y': 0, 'widt': 20, 'heig': height, 'skY': 30, 'fill': 'url(#gradient)'},
        {'x': 20, 'y': 22.91025543212891, 'widt': 20, 'heig': height, 'skY': -30, 'fill': 'url(#gradient)'}
    ];

    var group1 = svgElement.append('g').attr({
        'transform': 'translate(145,5) rotate(0, 20, 151.64102172851562)'
    });

    group1
        .selectAll('rect')
        .data(bar1ConstructorValues)
        .enter()
        .append('rect')
        .attr({
            'x': function (d) {
                return d.x;
            },
            'y': function (d) {
                return d.y;
            },
            'fill': function (d) {return d.fill},
            'stroke-width': 0,
            'stroke': 'rgb(0,0,0)',
            'width': function (d) {
                return d.widt;
            },
            'height': function (d) {
                return d.heig;
            },
            'transform': function (d) {
                return 'skewY(' + d.skY + ')'
            }
        });
}

//draw bar for handed in points
var draw_handed_in_points_badge = function(b) {

    //bar limit
    if (b.progress >= b.maximum) {
        b.progress = b.maximum
    }

    //console.log(b.progress);
    //setting height of bar according to progress
    height = 140 * (b.progress / b.maximum)

    var bar2ConstructorValues = [
        //bar 2 outlines
        //{'x': 0, 'y': 0, 'widt': 20, 'heig': 140, 'skY': 30, 'fill': 'green'},
        //{'x': 20, 'y': 22.91025543212891, 'widt': 20, 'heig': 140, 'skY': -30, 'fill': 'green'},
        //bar 2
        {'x': 0, 'y': 0, 'widt': 20, 'heig': height, 'skY': 30, 'fill': 'url(#gradient)'},
        {'x': 20, 'y': 22.91025543212891, 'widt': 20, 'heig': height, 'skY': -30, 'fill': 'url(#gradient)'}
    ];

    var group2 = svgElement.append('g').attr({
        'transform': 'translate(145,4) rotate(120, 20, 151.64102172851562)'
    });

    group2
        .selectAll('rect')
        .data(bar2ConstructorValues)
        .enter()
        .append('rect')
        .attr({
            'x': function (d) {
                return d.x;
            },
            'y': function (d) {
                return d.y;
            },
            'fill': function (d) {
                return d.fill
            },
            'stroke-width': 0,
            'stroke': 'rgb(0,0,0)',
            'width': function (d) {
                return d.widt;
            },
            'height': function (d) {
                return d.heig;
            },
            'transform': function (d) {
                return 'skewY(' + d.skY + ')'
            }
        });
}

//draw bar for evaluated points
var draw_evaluated_points_badge = function(b) {

    //bar limit
    if (b.progress >= b.maximum) {
        b.progress = b.maximum
    }

    //bar check fixed progress
    //b.progress = 60;

    //console.log(b.progress);

    if (b.progress > 40) {

        var heightScale = d3.scale.linear().domain([40,60]).range([163,280]);

        height = b.progress;

        scaledh = heightScale(height);

    } else {

        var heightScale = d3.scale.linear().domain([0,40]).range([0,140]);

        height = b.progress;
        scaledh = heightScale(height);
    }

    var bar3ConstructorValues = [
        //bar 3 outlines
        //{'x': 0, 'y': 0, 'widt': 20, 'heig': 280, 'skY': 30, 'fill': 'red'},
        //{'x': 20, 'y': 22.91025543212891, 'widt': 20, 'heig': 280, 'skY': -30, 'fill': 'red'},
        //bar 3
        {'x': 0, 'y': 0, 'widt': 20, 'heig': scaledh, 'skY': 30, 'fill': 'url(#gradient)'},
        {'x': 20, 'y': 22.91025543212891, 'widt': 20, 'heig': scaledh, 'skY': -30, 'fill': 'url(#gradient)'}
    ];


    var group3 = svgElement.append('g').attr({
        'transform': 'translate(146,4) rotate(240, 20, 151.64102172851562)'
    });
/*
    //tooltip div
    var tooltip = d3.select("#chart")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden")
	.text("Punkte erhalten");
*/
    group3
        .selectAll('rect')
        .data(bar3ConstructorValues)
        .enter()
        .append('rect')
        .attr({
            'x': function (d) {
                return d.x;
            },
            'y': function (d) {
                return d.y;
            },
            'fill': function (d) {
                return d.fill
            },
            'width': function (d) {
                return d.widt;
            },
            'height': function (d) {
                return d.heig;
            },
            'transform': function (d) {
                return 'skewY(' + d.skY + ')'
            }
        });


}


function drawBadges(){
    draw_evaluated_points_badge(svgData["badge_evaluated_points"]);
    draw_handed_in_points_badge(svgData["badge_handed_in_points"]);
    draw_all_chapter_badge(svgData["badge_all_chapter"]);
}

//console.log(svgData.badge_evaluated_points.maximum);


//checking conditions for grade bar above grade 4 - 'handed in badge' and 'evaluated points badge' are preconditions
if (svgData.badge_evaluated_points.progress >= svgData.badge_evaluated_points.maximum
    && svgData.badge_all_chapter.progress == svgData.badge_all_chapter.maximum
    && svgData.handed_in_points.progress == svgData.handed_in_points.maximum) {

    drawBadges();
} else if (svgData.badge_evaluated_points.progress > svgData.badge_evaluated_points.maximum) {

    svgData.badge_evaluated_points.progress = svgData.badge_evaluated_points.progress;
    drawBadges();
} else {
    drawBadges();
}

//definition of draw function for outlines
var pathFunction = d3.svg
    .line()
    .x(function(d) { return d.x})
    .y(function(d) { return d.y});

//grade indicator 4-3
svgElement.append('path').attr({
    'd': pathFunction(pathGradeSeperator3),
    'stroke-width': 1,
    'fill': 'none',
    'stroke': 'rgb(190,190,190)',
    'transform': 'translate(0,-25)'
});

//grade indicator 3-2
svgElement.append('path').attr({
    'd': pathFunction(pathGradeSeperator2),
    'stroke-width': 1,
    'fill': 'none',
    'stroke': 'rgb(190,190,190)',
    'transform': 'translate(0,-25)'
});

//draw outlines on svg viewport
svgElement.append('path').attr({
    'd': pathFunction(pathOutlineData),
    'stroke':'grey',
    'stroke-width': 1,
    'fill': 'none',
    'transform': 'translate(0,-25)'
});

//draw outlines for positive grade scale on svg viewport
svgElement.append('path').attr({
    'd': pathFunction(pathPosOutlineData),
    'stroke':'grey',
    'stroke-width': 1,
    'fill': 'none',
    'transform': 'translate(0,-25)'
});

//placing labels on svg viewport
svgElement
    .selectAll('text')
    .data(labelData)
    .enter()
    .append('text')
    .attr({
        'y': (function(d){return d.cy}),
        'x': (function(d){return d.cx}),
        'fill': 'black',
        'font-size': 14
    })
    .style('text-shadow', '1px 1px 1px #FFFFFF, -1px -1px 1px #FFFFFF, 1px -1px 1px #FFFFFF , -1px 1px 1px #FFFFFF') //#FF0000
    .text(function(d){return d.label;
});

//place img for awarded points
var imgs1 = svgElement.append("g")
    imgs1
        .append("svg:image")
        .attr("xlink:href", "/static/img/badges/badge_allchapter.png")
        .attr("x", "155")
        .attr("y", "28")
        .attr("width", "20")
        .attr("height", "20");

//place img for all chapter
var imgs2 = svgElement.append("g")
    imgs2
        .append("svg:image")
        .attr("xlink:href", "/static/img/badges/badge_ptsawarded.png")
        .attr("x", "55")
        .attr("y", "205")
        .attr("width", "20")
        .attr("height", "20");

//place img for points handed in
var imgs3 = svgElement.append("g")
    imgs3
        .append("svg:image")
        .attr("xlink:href", "/static/img/badges/badge_handedin.png")
        .attr("x", "255")
        .attr("y", "205")
        .attr("width", "20")
        .attr("height", "20");


/* depricated caption images
//place img for legend: all chapter
var imgs4 = svgElement.append("g")
    imgs4
        .append("svg:image")
        .attr("xlink:href", "/static/img/badges/badge_allchapter.png")
        .attr("x", "80")
        .attr("y", "290")
        .attr("width", "20")
        .attr("height", "20");

//place img for legend: points awarded
var imgs5 = svgElement.append("g")
    imgs5
        .append("svg:image")
        .attr("xlink:href", "/static/img/badges/badge_ptsawarded.png")
        .attr("x", "80")
        .attr("y", "320")
        .attr("width", "20")
        .attr("height", "20");

//place img for legend: points handed in
var imgs3 = svgElement.append("g")
    imgs3
        .append("svg:image")
        .attr("xlink:href", "/static/img/badges/badge_handedin.png")
        .attr("x", "80")
        .attr("y", "350")
        .attr("width", "20")
        .attr("height", "20");
*/