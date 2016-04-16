function department_pie(data){
  console.log(data);
  var pie = new d3pie("pie", {
        "size": {
        "canvasHeight": 400,
		"canvasWidth": 500,
		"pieOuterRadius": "90%"
	},
  data:{
    "sortOrder": "value-desc",
    "content":data},
  tooltips: {
    enabled: true,
    type: "placeholder",
    string: "{label}: {percentage}%",
    styles: {
      fadeInSpeed: 500,
      backgroundColor: "#00cc99",
      backgroundOpacity: 0.8,
      color: "#ffffcc",
      borderRadius: 4,
      font: "verdana",
      fontSize: 20,
      padding: 20
    }
  }
});

}

function set_slider(){
  d3.select('#slider3').call(d3.slider()
  .axis(true).min(2004).max(2016).step(0.5)
  // .on("slide", function(evt, value) {
  //
  //     console.log("here");
  //     console.log(value);
  //     if(value === 1999 || value === 2000){
  //         $.ajax({ // ajax call for revision data for file is mades
  //                 url: '/year',
  //                 data: JSON.stringify({ // data that is sent to the flask server
  //                     state: curr_state,
  //                     year: value
  //                 }),
  //                 type: 'POST',
  //                 contentType: 'application/json;charset=UTF-8',
  //                 success: function(response) { // response that is sent back from the flask server
  //                     if (response['msg'] === 'YES') {
  //                         console.log("PRINTING AJAX RESPONSE");
  //                         console.log("YES");
  //                         console.log(response);
  //
  //
  //                         //$('#slider3').empty();
  //                         started = true;
  //                         init(response['data'], response['min'], response['max']);
  //                         $("#info span").text("Total Number of Immigrants : " + response['total']);
  //                     }
  //                 },
  //                 dataType: "json",
  //                 error: function(error) {
  //                     console.log("ERROR")
  //                     console.log(error); // log error on invalid ajax request
  //                 }
  //             });
  //
  //     }})


  );

}

