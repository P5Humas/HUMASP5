// Chart1
var options = {
    series: [
      {
        name: "Net Profit",
        data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
      },
      {
        name: "Revenue",
        data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
      },
    ],
    chart: {
      type: "bar",
      height: 350,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "55%",
        borderRadius: 5,
        borderRadiusApplication: "end",
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ["transparent"],
    },
    xaxis: {
      categories: ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
    },
  
    fill: {
      opacity: 1,
    },
    tooltip: {
      y: {
        formatter: function (val) {
          return "$ " + val + " thousands";
        },
      },
    },
  };
  
  var chart = new ApexCharts(document.querySelector("#Chart1"), options);
  chart.render();
  
  // Chart2
  var options = {
    series: [44, 55, 13, 33],
    chart: {
      width: "75%",
      type: "donut",
    },
    colors: ['#008ffb', '#00e396', '#feb019'], 
    dataLabels: {
      enabled: false,
    },
    legend: {
      position: "left",
      offsetY: 0,
      offsetX: 0,
      height: 230,
    },
  };
  
  var chart = new ApexCharts(document.querySelector("#Chart2"), options);
  chart.render();
  
  function appendData() {
    var arr = chart.w.globals.series.slice();
    arr.push(Math.floor(Math.random() * (100 - 1 + 1)) + 1);
    return arr;
  }
  
  function removeData() {
    var arr = chart.w.globals.series.slice();
    arr.pop();
    return arr;
  }
  
  function randomize() {
    return chart.w.globals.series.map(function () {
      return Math.floor(Math.random() * (100 - 1 + 1)) + 1;
    });
  }
  
  function reset() {
    return options.series;
  }
  
  document.querySelector("#randomize").addEventListener("click", function () {
    chart.updateSeries(randomize());
  });
  
  document.querySelector("#add").addEventListener("click", function () {
    chart.updateSeries(appendData());
  });
  
  document.querySelector("#remove").addEventListener("click", function () {
    chart.updateSeries(removeData());
  });
  
  document.querySelector("#reset").addEventListener("click", function () {
    chart.updateSeries(reset());
  });

  // Chart 3
  var options = {
    series: [
      {
        name: "series1",
        data: [31, 40, 28, 51, 42, 109, 100],
      },
      {
        name: "series2",
        data: [11, 32, 45, 32, 34, 52, 41],
      },
    ],
    chart: {
      height: 350,
      type: "area",
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
    },
    xaxis: {
      type: "datetime",
      categories: [
        "2018-09-19T00:00:00.000Z",
        "2018-09-19T01:30:00.000Z",
        "2018-09-19T02:30:00.000Z",
        "2018-09-19T03:30:00.000Z",
        "2018-09-19T04:30:00.000Z",
        "2018-09-19T05:30:00.000Z",
        "2018-09-19T06:30:00.000Z",
      ],
    },
    tooltip: {
      x: {
        format: "dd/MM/yy HH:mm",
      },
    },
  };

  var chart = new ApexCharts(document.querySelector("#Chart3"), options);
  chart.render();

  // Chart 4
  var options = {
    series: [
      {
        name: "Desktops",
        data: [10, 41, 35, 51, 49, 62, 69, 91, 148],
      },
    ],
    chart: {
      height: 350,
      type: "line",
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "straight",
    },
    title: {
      text: "Product Trends by Month",
      align: "left",
    },
    grid: {
      row: {
        colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
      ],
    },
  };

  var chart = new ApexCharts(document.querySelector("#Chart4"), options);
  chart.render();
  