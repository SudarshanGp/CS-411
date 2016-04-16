var pie = new d3pie("pie", {
  data: {
    content: [
      { label: "Elephants", value: 1 },
      { label: "Motmots", value: 2 },
      { label: "Pikas", value: 3 },
      { label: "Jays", value: 2 },
      { label: "Rhubarb", value: 5 },
      { label: "Tennis", value: 2 },
      { label: "Chickens", value: 1 }
    ]
  },
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