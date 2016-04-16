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

