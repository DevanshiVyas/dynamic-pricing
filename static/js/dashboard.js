var ctx = document.getElementById("product-chart");

var getRandom = function() {
    var d = [], i;
    for (i = 0; i < 7; i++) {
        d.push(Math.round(Math.random(1) * 100));
    }
    return d;
}

var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "iPhone 5S",
            backgroundColor: "rgba(255,99,132,0.6)",
            borderColor: "rgba(255,99,132,1)",
            data: getRandom()
        },
        {
            label: "iPhone 4S",
            backgroundColor: "rgba(255,199,32,0.6)",
            borderColor: "rgba(255,199,32,1)",
            data: getRandom()
        },
        {
            label: "Kindle",
            backgroundColor: "rgba(125,99,132,0.6)",
            borderColor: "rgba(125,99,132,1)",
            data: getRandom()
        },
        {
            label: "Nook",
            backgroundColor: "rgba(25,299,32,0.6)",
            borderColor: "rgba(25,299,32,1)",
            data: getRandom()
        }
    ]
};

var myChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

$("[type='checkbox']").bootstrapSwitch();
